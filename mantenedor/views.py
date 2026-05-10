from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Fabricante, User
from gestion_tickets.forms import FabricanteForm
from gestion_tickets.models import Ticket
from django.http import HttpResponse
import datetime
from django.template.loader import get_template
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
