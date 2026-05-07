from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Avg, F #estadisticas
from .models import Ticket, Mensaje, Fabricante
from django.contrib.auth.models import User, Group
from .forms import TicketForm, MensajeForm, FabricanteForm
import datetime
from django.utils import timezone
import holidays
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



def is_soporte_or_admin(user):
    return user.groups.filter(name__in=['Soporte', 'Administrador']).exists()



# Definir feriados de Chile (puedes cambiar a otro país si es necesario)
feriados = holidays.Chile(years=[2025, 2026])

def sumar_horas_habiles(fecha_inicio, horas):
    fecha = fecha_inicio
    horas_restantes = horas

    while horas_restantes > 0:
        fecha += datetime.timedelta(hours=1)

        # Si es fin de semana o feriado, saltar
        if fecha.weekday() >= 5 or fecha.date() in feriados:
            continue

        horas_restantes -= 1

    return fecha



#pagina de inicio home

#@login_required
def home(request):
    #if request.user.rol == 'cliente' or request.user.rol == 'integrador' or request.user.rol == 'vendedor' or request.user.rol == 'soporte':
        #return redirect('home')
    #elif is_soporte_or_admin(request.user):
        #return redirect('dashboard')
    return render(request, 'home.html')





@login_required
def listar_tickets(request):
    user = request.user
  
    if user.groups.filter(name="Integrador").exists() or user.groups.filter(name="Cliente").exists():
        # Solo ve sus propios tickets
        tickets = Ticket.objects.filter(usuario = user)  # Asegúrate que tu modelo Ticket tenga FK a usuario
    elif user.groups.filter(name="Soporte").exists() or user.groups.filter(name="Administrador").exists():
        # Puede ver todos los tickets
        tickets = Ticket.objects.all()
    else:
        # Usuario sin permisos
        tickets = Ticket.objects.none()
        

    context = {'tickets': tickets}
    return render(request, 'listarTicket.html', context)



@login_required
def detalle_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Validar permisos
    if not (ticket.usuario == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, 'No tienes permiso para ver este ticket.')
        return redirect('login')

    mensajes = Mensaje.objects.filter(ticket=ticket)

    # Evitar agregar mensajes si el ticket está cerrado
    if request.method == 'POST':
        if ticket.estado == "Cerrado":
            messages.warning(request, "Este ticket está cerrado. No puedes agregar nuevos mensajes.")
            return redirect('detalle_ticket', pk=pk)

        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Mensaje.objects.create(
                ticket=ticket,
                usuario=request.user,
                contenido=contenido
            )
            ticket.ultima_actualizacion = timezone.now()
            ticket.save()

            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('detalle_ticket', pk=pk)
        else:
            messages.error(request, 'No puedes enviar un mensaje vacío.')

    context = {
        'ticket': ticket,
        'mensajes': mensajes,
    }
    return render(request, 'detalleTicket.html', context)



@login_required
def cerrar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    #if not (request.usuario.rol in ['Soporte', 'Administrador'] or request.user.is_superuser):
    if not (ticket.usuario == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, "No tienes permisos para cerrar tickets.")
        return redirect('detalle_ticket', pk=pk)

    ticket.estado = "cerrado"
    ticket.ultima_actualizacion = timezone.now()
    ticket.save()

    messages.success(request, f"El ticket #{ticket.id} ha sido cerrado correctamente.")
    return redirect('detalle_ticket', pk=pk)


@login_required
def abrir_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    #if not (request.usuario.rol in ['Soporte', 'Administrador'] or request.user.is_superuser):
    if not (ticket.usuario == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, "No tienes permisos para abrir este tickets.")
        return redirect('detalle_ticket', pk=pk)

    ticket.estado = "abierto"
    ticket.ultima_actualizacion = timezone.now()
    ticket.save()

    messages.success(request, f"El ticket #{ticket.id} ha sido abierto correctamente.")
    return redirect('detalle_ticket', pk=pk)




@login_required
def crear_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            # Establecer fecha de respuesta esperada (ejemplo: 48 horas después de la creación)
            inicio = timezone.now()
            ticket.fecha_respuesta_esperada = sumar_horas_habiles(inicio, 72)
            ticket.save()
            messages.success(request, 'Ticket creado exitosamente.')

            # Notificar al equipo de soporte sobre el nuevo ticket (ejemplo)
            # send_mail(
            #     f'Nuevo Ticket Creado: {ticket.asunto}',
            #     f'Un nuevo ticket ha sido creado por {request.user}. Asunto: {ticket.asunto}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     ['soporte@grupoalmma.cl'], # Reemplazar con el correo del equipo de soporte
            #     fail_silently=False,
            # )
            
            return redirect('listar_ticket')
        
    else:
        form = TicketForm()
    return render(request, 'crearTicket.html', {'form': form})



# vista para detalle de sla del ticket


def sla_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Calcular SLA si no está definido
    if not ticket.fecha_respuesta_esperada:
        ticket.calcular_sla()

    mensajes = ticket.mensajes.all()

    context = {
        'ticket': ticket,
        'mensajes': mensajes,
        'cumplimiento_respuesta': ticket.cumplimiento_respuesta(),
        'cumplimiento_resolucion': ticket.cumplimiento_resolucion(),
    }
    return render(request, 'detalleTicket.html', context)









#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX




@login_required
def ver_ticket(request):
    if request.user.rol == 'username' or request.user.rol == 'integrador':
        tickets = Ticket.objects.filter(cliente=request.user)
    else:
        messages.error(request, 'No tienes permiso para ver los tickets.')
        return redirect('lista_tickets')

    context = {'tickets': tickets}
    return render(request, 'gestion_tickets/ticket_list_cliente.html', context)





@login_required
def enviar_mensaje(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Asegurar que solo el dueño del ticket o soporte/admin pueda enviar mensajes
    if not (ticket.usuario == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, 'No tienes permiso para enviar mensajes en este ticket.')
        return redirect('listaTicket')

    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Mensaje.objects.create(
                ticket=ticket,
                usuario=request.user,
                contenido=contenido,
                es_respuesta=True  # opcional, si quieres marcarlo
            )
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('detalleTicket', pk=pk)
        else:
            messages.error(request, 'El mensaje no puede estar vacío.')

    return render(request, 'listarTicket.html', {'ticket': ticket})



@login_required
def listar_mensajes(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Asegurar que solo el cliente/integrador o el personal de soporte/admin pueda ver los mensajes
    if not (ticket.usuario == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, 'No tienes permiso para ver los mensajes de este ticket.')
        return redirect('listaTickets')

    mensajes = Mensaje.objects.filter(ticket=ticket)
    context = {'ticket': ticket, 'mensajes': mensajes}
    return render(request, 'gestion_tickets/listar_mensajes.html', context) 




@user_passes_test(is_soporte_or_admin) # Solo soporte y admin pueden editar
def editar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket actualizado exitosamente.')
            return redirect('detalle_ticket', pk=pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'editarTicket.html', {'form': form, 'ticket': ticket})


