from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Fabricante, User
from gestion_tickets.forms import FabricanteForm
from gestion_tickets.models import Ticket
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from gestion_tickets.views import is_soporte_or_admin




# Create your views here.



def is_admin(user):
    return user.rol == 'admin'


@login_required
@user_passes_test(is_admin) # Solo administradores
def admin_panel(request):
    # Aquí podrías listar usuarios, fabricantes, etc. para su administración
    usuarios = User.objects.all()
    fabricantes = Fabricante.objects.all()
    context = {
        'usuarios': usuarios,
        'fabricantes': fabricantes,
    }
    return render(request, 'gestion_tickets/admin_panel.html', context)




# --- Generación de Reportes en PDF ---
@login_required
@user_passes_test(is_soporte_or_admin)
def generar_reporte_pdf(request):
    # Filtros para el reporte
    cliente_id = request.GET.get('cliente')
    fabricante_id = request.GET.get('fabricante')
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')

    tickets = Ticket.objects.all()

    if cliente_id:
        tickets = tickets.filter(cliente__id=cliente_id)
    if fabricante_id:
        tickets = tickets.filter(fabricante__id=fabricante_id)
    if fecha_inicio_str:
        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            tickets = tickets.filter(fecha_creacion__gte=fecha_inicio)
        except ValueError:
            pass # Manejar error de formato de fecha
    if fecha_fin_str:
        try:
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            tickets = tickets.filter(fecha_creacion__lte=fecha_fin + datetime.timedelta(days=1)) # Incluir todo el día
        except ValueError:
            pass

    template_path = 'gestion_tickets/reporte_tickets_pdf.html' # Plantilla HTML para el PDF
    context = {'tickets': tickets, 'fecha_generacion': timezone.now()}

    # Renderizar la plantilla HTML
    template = get_template(template_path)
    html = template.render(context)

    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_tickets.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response





# --- Vistas de Fabricantes ---


@login_required
def crear_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fabricante creado exitosamente.')
            return redirect('lista_fabricantes')
    else:
        form = FabricanteForm()
    return render(request, 'gestion_tickets/fabricante_form.html', {'form': form})  


@login_required
def editar_fabricante(request, pk):
    fabricante = get_object_or_404(Fabricante, pk=pk)
    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fabricante actualizado exitosamente.')
            return redirect('lista_fabricantes')
    else:
        form = FabricanteForm(instance=fabricante)
    return render(request, 'gestion_tickets/fabricante_form.html', {'form': form, 'fabricante': fabricante})    


@login_required
def eliminar_fabricante(request, pk):
    fabricante = get_object_or_404(Fabricante, pk=pk)
    if request.method == 'POST':
        fabricante.delete()
        messages.success(request, 'Fabricante eliminado exitosamente.')
        return redirect('lista_fabricantes')
    return render(request, 'gestion_tickets/fabricante_confirm_delete.html', {'fabricante': fabricante})


def generar_pdf_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    # Asegurar que solo el cliente/integrador o el personal de soporte/admin pueda generar el PDF
    if not (ticket.cliente == request.user or is_soporte_or_admin(request.user)):
        messages.error(request, 'No tienes permiso para generar un PDF de este ticket.')
        return redirect('lista_tickets')

    template_path = 'gestion_tickets/ticket_pdf.html'
    context = {'ticket': ticket, 'fecha_generacion': timezone.now()}

    # Renderizar la plantilla HTML
    template = get_template(template_path)
    html = template.render(context)

    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response 


