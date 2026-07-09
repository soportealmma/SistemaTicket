from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .models import Perfil
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin       
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from .models import Usuario, Perfil
from .forms import UsuarioForm, UsuarioEditarForm, PerfilForm
from django.contrib.admin.views.decorators import staff_member_required




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
    return render(request, 'login/login.html', {'form': form})




def listar_usuarios(request):
    usuarios = Usuario.objects.all().order_by("first_name")
    return render(request, "usuarios/listar.html", {"usuarios": usuarios})

def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()

            # Asignar grupos
            usuario.groups.set(form.cleaned_data["grupos"])

            # Crear perfil
            Perfil.objects.create(
                user=usuario,
                rut=form.cleaned_data["rut"],
                telefono=form.cleaned_data["telefono"],
                cargo=form.cleaned_data["cargo"],
                area=form.cleaned_data["area"],
            )

            return redirect("listar_usuarios")
    else:
        form = UsuarioForm()

    return render(request, "usuarios/crear.html", {"form": form})


def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    perfil = usuario.perfil

    if request.method == "POST":
        form_user = UsuarioEditarForm(request.POST, instance=usuario)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=perfil)

        if form_user.is_valid() and form_perfil.is_valid():
            form_user.save()
            form_perfil.save()

            usuario.groups.set(form_user.cleaned_data["grupos"])

            return redirect("listar_usuarios")

    else:
        form_user = UsuarioEditarForm(instance=usuario)
        form_user.fields["grupos"].initial = usuario.groups.all()
        form_perfil = PerfilForm(instance=perfil)

    return render(request, "usuarios/editar.html", {
        "form_user": form_user,
        "form_perfil": form_perfil,
        "usuario": usuario
    })



def cambiar_estado_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect("listar_usuarios")


def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)
    usuario.delete()
    return redirect("listar_usuarios")




@staff_member_required
def dashboard_mantenedor(request):
    return render(request, "usuarios/mantenedor_dashboard.html")




def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'usuarios/dashboard.html', {'user': request.user})
    else:
        messages.error(request, "Debes iniciar sesión para acceder al dashboard.")
        return redirect('login')