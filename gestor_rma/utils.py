from django.utils import timezone
from .models import SolicitudRMA

def generar_numero_rma():
    año_mes = timezone.now().strftime("%Y%m")
    ultimo = SolicitudRMA.objects.filter(
        fecha_solicitud__year=timezone.now().year
    ).count() + 1
    return f"{año_mes}-{ultimo:05d}"
