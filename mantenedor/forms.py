from django import forms
from django.contrib.auth.models import User
from .models import Fabricante


class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'nombre': 'Nombre del Fabricante',
            'descripcion': 'Descripción (opcional)',
        }