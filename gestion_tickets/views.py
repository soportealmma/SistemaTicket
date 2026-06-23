from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Avg, F
from .models import Ticket, Mensaje, TicketImagen
from gestor_rma.models import SolicitudRMA
from django.contrib.auth.models import User, Group
from .forms import TicketForm, MensajeForm, TicketUpdateForm, TicketImagenForm
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
import tempfile
from io import BytesIO





def is_soporte_or_admin(user):
    return user.groups.filter(name__in=['Soporte', 'Administrador', 'staff']).exists()




#pagina de inicio home

#@login_required
def home(request):
    return render(request, 'home/home.html')


@login_required
def listar_tickets(request):
    user = request.user
  
    if user.groups.filter(name="Integrador").exists() or user.groups.filter(name="Cliente").exists():
        # Solo ve sus propios tickets
        #tickets = Ticket.objects.filter(username = user)  # Asegúrate que tu modelo Ticket tenga FK a usuario
    #elif user.groups.filter(name="Soporte").exists() or user.groups.filter(name="Administrador").exists():
        # Puede ver todos los tickets
        tickets = Ticket.objects.all()
    else:
        # Usuario sin permisos
        tickets = Ticket.objects.none()
        

    context = {'tickets': tickets}
    return render(request, 'tickets/listarTicket.html', context)



@login_required
def detalle_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    mensajes = ticket.mensajes.all()
    imagenes = ticket.imagenes.all()
    rma = SolicitudRMA.objects.filter(ticket_origen = ticket).first()

    if request.method == "POST":
        contenido = request.POST.get("contenido")

        if contenido:
            Mensaje.objects.create(
                ticket=ticket,
                usuario=request.user,
                contenido=contenido
            )

        # Si soporte cambia estado
        if request.user.is_superuser or getattr(request.user, "rol", None) == "Soporte":
            nuevo_estado = request.POST.get("estado")
            if nuevo_estado:
                ticket.estado = nuevo_estado
                ticket.save()

        return redirect("detalle_ticket", pk=pk)

    update_form = TicketUpdateForm(instance=ticket)

    return render(request, "tickets/detalleTicket.html", {
        "ticket": ticket,
        "mensajes": mensajes,
        "update_form": update_form,
        "imagenes": imagenes,
        "rma": rma,
    })



@login_required
def cerrar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Solo soporte o admin pueden cerrar tickets
    if not is_soporte_or_admin(request.user):
        messages.error(request, "No tienes permisos para cerrar tickets.")
        return redirect('detalle_ticket', pk=pk)

    ticket.estado = "cerrado"
    ticket.fecha_cierre = timezone.now()
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


def crear_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.save()

            fecha_actual = timezone.now()
            if fecha_actual.weekday() == 4 or 3:
                ticket.fecha_respuesta = fecha_actual + timedelta(days=5)
            else:
                ticket.fecha_respuesta = fecha_actual + timedelta(days=2)
            ticket.save()

            # Procesar imágenes dinámicas
            for key in request.FILES:
                if key.startswith("imagen_"):
                    numero = key.split("_")[1]
                    descripcion = request.POST.get(f"descripcion_{numero}", "")

                    TicketImagen.objects.create(
                        ticket=ticket,
                        imagen=request.FILES[key],
                        descripcion=descripcion
                    )

            messages.success(request, "Ticket creado exitosamente.")
            return redirect("listar_ticket")

    else:
        form = TicketForm()

    return render(request, "tickets/crearTicket.html", {"form": form})




def exportar_ticket_pdf(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    imagenes = ticket.imagenes.all()
    mensajes = Mensaje.objects.filter(ticket=ticket).order_by("fecha_envio")

    html_string = render_to_string("tickets/ticket_pdf.html", {
        "ticket": ticket,
        "imagenes": imagenes,
        'mensajes': mensajes,
    })

    # Crear PDF en memoria (sin archivos temporales)
    pdf_file = BytesIO()
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        target=pdf_file,
        stylesheets=[CSS(string="""
            @page { size: letter; margin: 20mm; }
            body { font-family: sans-serif; }
            img { max-width: 300px; margin-bottom: 10px; }
        """)]
    )

    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="ticket_{ticket.id}.pdf"'
    return response


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
    return render(request, 'tickets/detalleTicket.html', context)

# revisar esta vista ################
@login_required
def ver_ticket(request):
    if request.user.rol == 'username' or request.user.rol == 'integrador':
        tickets = Ticket.objects.filter(cliente=request.user)
    else:
        messages.error(request, 'No tienes permiso para ver los tickets.')
        return redirect('lista_tickets')

    context = {'tickets': tickets}
    return render(request, 'gestion_tickets/ticket_list_cliente.html', context)
# #############################################




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

    return render(request, 'tickets/listarTicket.html', {'ticket': ticket})



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




@login_required
def editar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if not request.user.is_staff:
        messages.error(request, "No tiene permisos para editar tickets, verifique con su administrador")
    else:
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ticket actualizado exitosamente.')
                return redirect('detalle_ticket', pk=pk)
        else:
            form = TicketForm(instance=ticket)
        return render(request, 'tickets/editarTicket.html', {'form': form, 'ticket': ticket})


