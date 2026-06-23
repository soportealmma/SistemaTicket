from django import forms
from django.contrib.auth.models import User 
from .models import Ticket, Mensaje, TicketImagen



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket  
        fields = "__all__"
        exclude = ['fecha_creacion', 'estado']



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



class TicketSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Buscar")

    estado = forms.ChoiceField(
        choices=[("", "Todos")] + Ticket.ESTADO_CHOICES,
        required=False,
        label="Estado"
    )

class TicketFilterForm(forms.Form):
    estado = forms.ChoiceField(
        choices=[("", "Todos")] + Ticket.ESTADO_CHOICES,
        required=False,
        label="Estado"
    )


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["estado"]  # Solo el campo que realmente existe en tu modelo
        widgets = {
            "estado": forms.Select(attrs={
                "class": "shadow border rounded w-full p-2"
            }),
        }



class TicketImagenForm(forms.ModelForm):
    class Meta:
        model = TicketImagen
        fields = ["imagen"]
        exclude = ["fecha_subida", "descripcion"]  # Excluir el campo de relación, se asignará en la vista


