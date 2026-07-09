from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Usuario, Perfil

class UsuarioForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Roles"
    )

    rut = forms.CharField(label="RUT")
    telefono = forms.CharField(required=False)
    cargo = forms.CharField(required=False)
    area = forms.CharField(required=False)

    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email", "password1", "password2"]


class UsuarioEditarForm(forms.ModelForm):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Roles"
    )

    class Meta:
        model = Usuario
        fields = ["first_name", "last_name", "email", "is_active"]


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ["rut", "telefono", "cargo", "area", "foto", "fecha_ingreso"]
