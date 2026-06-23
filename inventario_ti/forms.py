from django import forms
from .models import EquipoTI, CelularTI, LicenciaTI, HistorialAsignacion, EquipoTI, CelularTI, LicenciaTI
from django import forms
from django.contrib.auth.models import User


class EquipoTIForm(forms.ModelForm):
    class Meta:
        model = EquipoTI
        fields = [
            "tipo_equipo", "marca", "modelo", "numero_serie",
            "cpu", "ram_gb", "tipo_disco", "capacidad_disco_gb",
            "sistema_operativo", "licencia_windows_key",
            "accesorios", "estado_equipo", "responsable_actual"
        ]

        widgets = {
            "accesorios": forms.Textarea(attrs={"rows": 3}),
        }


class CelularTIForm(forms.ModelForm):
    class Meta:
        model = CelularTI
        fields = [
            "marca", "modelo","numero_serie", "imei1", "imei2",
            "numero_sim1", "numero_sim2",
            "version_os", "clave_bloqueo",
            "estado", "responsable_actual"
        ]


class LicenciaTIForm(forms.ModelForm):
    class Meta:
        model = LicenciaTI
        fields = [
            "tipo_licencia", "producto", "clave",
            "correo_asociado", "fecha_compra", "fecha_expiracion",
            "responsable_actual"
        ]



#----ASIGNACIÓN -------#


class AsignacionForm(forms.ModelForm):

    equipo = forms.ModelChoiceField(
        queryset=EquipoTI.objects.all(),
        required=False,
        label="Equipo"
    )

    celular = forms.ModelChoiceField(
        queryset=CelularTI.objects.all(),
        required=False,
        label="Celular"
    )

    licencia = forms.ModelChoiceField(
        queryset=LicenciaTI.objects.all(),
        required=False,
        label="Licencia"
    )

    persona = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label="Responsable"
    )

    class Meta:
        model = HistorialAsignacion
        fields = [
            "persona",
            "equipo",
            "celular",
            "licencia",
            "fecha_inicio",
            "fecha_termino",
            "motivo_termino",
            "observaciones",
        ]

#================================
#---DEVOLUCION DE ASIGNACIONES---
#================================

class DevolucionForm(forms.Form):
    equipos = forms.ModelMultipleChoiceField(
        queryset=EquipoTI.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Equipos a devolver"
    )

    celulares = forms.ModelMultipleChoiceField(
        queryset=CelularTI.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Celulares a devolver"
    )

    licencias = forms.ModelMultipleChoiceField(
        queryset=LicenciaTI.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Licencias a devolver"
    )

    motivo = forms.ChoiceField(
        choices=[
            ("renuncia", "Renuncia"),
            ("despido", "Despido"),
            ("falla", "Falla del equipo"),
            ("renovacion", "Renovación"),
            ("otro", "Otro"),
        ],
        required=True
    )

    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False
    )
