from django import forms
from django.contrib.auth.models import User
from .models import SolicitudRMA, ResolucionRMA, RMAImagen


#--- Formulario para RMA ---



class RMAImagenForm(forms.ModelForm):
    class Meta:
        model = RMAImagen
        fields = ["imagen", "descripcion"]




class SolicitudRMAForm(forms.ModelForm):
    class Meta:
        model = SolicitudRMA
        fields = '__all__'
        exclude = ['fecha_solicitud', 'estado', 'usuario_solicita', 'numero_rma']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Siempre mostrar, pero no editable
        #self.fields['numero_rma'].widget.attrs['readonly'] = True





class ResolucionRMAForm(forms.ModelForm):
    class Meta:
        model = ResolucionRMA
        fields = [
            "ingeniero_responsable",
            "condicion_fisica",
            "sellos_intactos",
            "accesorios_recibidos",
            "descripcion_falla",
            "observaciones",
            "diagnostico",
            "causa_raiz",
            "aplica_garantia",
            "motivo_no_garantia",
        ]

