from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .models import Perfil
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin       
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import get_user_model
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UsuarioForm, UsuarioUpdateForm, LoginForm
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # redirige donde necesites
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})







def es_admin(user):
    return user.is_superuser or user.is_staff # O también podrías usar un grupo especial

@user_passes_test(es_admin)
def cambiar_grupo_usuario(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    grupos = Group.objects.all()

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo')
        grupo = Group.objects.get(id=grupo_id)
        perfil.grupo = grupo
        perfil.save()
        return redirect('listar_usuarios')  # O donde quieras

    return render(request, 'cambiar_grupo.html', {'perfil': perfil, 'grupos': grupos})


# usuarios/views.py

def createUsuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # 1️⃣ Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Solo si tu form pide contraseña
            user.save()

            # 2️⃣ Asignar al grupo "Integrador" por defecto
            grupo_defecto, _ = Group.objects.get_or_create(name="Integrador")
            user.groups.add(grupo_defecto)

            # 3️⃣ Crear o actualizar el perfil
            perfil, created = Perfil.objects.get_or_create(
                user=user,
                defaults={'grupo': grupo_defecto}
            )
            if not created:
                perfil.grupo = grupo_defecto
                perfil.save()

            return redirect('login')  # O donde quieras redirigir
    else:
        form = UsuarioForm()

    return render(request, 'createUsuario.html', {'form': form})



def updateUsuario(request, pk):
    usuario = get_user_model().objects.get(pk=pk)
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado exitosamente.")
            return redirect('usuario_list')
    else:
        form = UsuarioUpdateForm(instance=usuario)
    return render(request, 'usuarios/usuario_form.html', {'form': form})

def deleteUsuario(request, pk):
    usuario = get_user_model().objects.get(pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('usuario_list')
    return render(request, 'usuarios/usuario_confirm_delete.html', {'usuario': usuario})


def listUsuarios(request):
    usuarios = get_user_model().objects.all()
    return render(request, 'listarUsuarios.html', {'usuarios': usuarios})


#@login_required
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html', {'user': request.user})
    else:
        messages.error(request, "Debes iniciar sesión para acceder al dashboard.")
        return redirect('login')