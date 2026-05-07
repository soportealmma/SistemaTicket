from django import forms
from django.contrib.auth.models import User 
from .models import Ticket, Mensaje, Fabricante 

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['asunto', 'descripcion', 'fabricante', 'prioridad', 'fecha_respuesta_esperada']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'fecha_respuesta_esperada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'asunto': 'Asunto',
            'descripcion': 'Descripción',
            'fabricante': 'Fabricante',
            'prioridad': 'Prioridad',
            'fecha_respuesta_esperada': 'Fecha de Registro',
        }

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 6}),
        }
        labels = {
            'contenido': 'Mensaje',
        }

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

class TicketSearchForm(forms.Form):
    asunto = forms.CharField(required=False, label='Asunto')
    estado = forms.ChoiceField(choices=Ticket.ESTADOS, required=False, label='Estado')
    prioridad = forms.ChoiceField(choices=Ticket.PRIORIDADES, required=False, label='Prioridad')
    fecha_creacion_desde = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Fecha de Creación Desde')
    fecha_creacion_hasta = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Fecha de Creación Hasta')


class TicketFilterForm(forms.Form):

    cliente = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Cliente/Integrador',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    asignado_a = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label='Asignado a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    estado = forms.ChoiceField(
        choices=Ticket.ESTADOS,
        required=False,
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    prioridad = forms.ChoiceField(
        choices=Ticket.PRIORIDADES,
        required=False,
        label='Prioridad',
        widget=forms.Select(attrs={'class': 'form-control'})
    )   

