from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from django.contrib import messages
from django.core.exceptions import ValidationError  




# forms.py

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'})
    )
    remember_me = forms.BooleanField(required=False, initial=False)



# usuarios/forms.py


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
 

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("La contraseña debe contener al menos un dígito.")
        if not any(char.isalpha() for char in password):
            raise ValidationError("La contraseña debe contener al menos una letra.")
        return password
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            messages.success(self.request, "Usuario creado exitosamente.")
        return user

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre (opcional)'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido (opcional)'}),
        }
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("El correo electrónico ya está en uso.")
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            messages.success(self.request, "Usuario actualizado exitosamente.")
        return user
    



# gestion_tickets/forms.py
from django import forms
from django.contrib.auth.models import User

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
