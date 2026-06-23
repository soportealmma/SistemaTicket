from django import forms
from .models import Tarea, TareaMensaje

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = [
            "titulo",
            "descripcion",
            "fecha_compromiso",
            "criticidad",
            "estado",
            "responsable",
            "area", 
            "observaciones",
        ]

        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Título de la tarea"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descripción detallada"
            }),
            "fecha_compromiso": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "criticidad": forms.Select(attrs={
                "class": "form-select"
            }),
            "estado": forms.Select(attrs={
                "class": "form-select"
            }),
            "responsable": forms.Select(attrs={
                "class": "form-select"
            }),
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Observaciones internas"
            }),
            "area": forms.Select(attrs={"class": "form-select"}),

        }


class TareaMensajeForm(forms.ModelForm):
    class Meta:
        model = TareaMensaje
        fields = ["mensaje"]

        widgets = {
            "mensaje": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Escribe un mensaje..."
            }),
        }
