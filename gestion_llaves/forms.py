# gestion_llaves/forms.py
from django import forms
from .models import LlaveLicencia, HistorialLicencia

#class LlaveLicenciaForm(forms.ModelForm):
    #class Meta:
        #model = LlaveLicencia
       # fields = [
      #      "rut", "cliente", "contacto", "tipo_llave",
      #      "numero_serie", "fecha_vencimiento", "historial_pagos"
      #  ]
       # exclude = ['fecha_registro']
      #  widgets = {
       #     "fecha_vencimiento": forms.DateInput(attrs={"type": "date"}),
       #     "historial_pagos": forms.Textarea(attrs={"rows": 3}),
       # }
class RegistroLlaveForm(forms.ModelForm):
    class Meta:
        model = LlaveLicencia
        fields = "__all__"
        exclude = ["fecha_registro"]


#class RegistroLlaveForm(forms.form):
   # rut = forms.CharField(max_length=12)
    #cliente = forms.CharField(max_length=200)
    #contacto = forms.CharField(max_length=200)
    #tipo_llave = forms.ChoiceField(choices=LlaveLicencia.TIPO_LLAVE)
   # numero_serie = forms.CharField(max_length=100)
    #fecha_vencimiento = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

   # tipo_documento = forms.ChoiceField(choices=HistorialLicencia.TIPO_DOC)
   # numero_documento = forms.CharField(max_length=50)
   # observaciones = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
