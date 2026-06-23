from django.db import models
from django.utils import timezone

class LlaveLicencia(models.Model):
    TIPO_LLAVE = [
        ("WIBU", "WIBU"),
        ("ESD", "ESD"),
    ]

    rut = models.CharField(max_length=12)
    fecha_registro = models.DateField(default=timezone.now)
    cliente = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    tipo_llave = models.CharField(max_length=10, choices=TIPO_LLAVE)
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_vencimiento = models.DateField()

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def dias_para_vencer(self):
        return (self.fecha_vencimiento - timezone.now().date()).days

    def esta_por_vencer(self):
        return self.dias_para_vencer() <= 5

    def __str__(self):
        return f"{self.numero_serie} - {self.cliente}"


class HistorialLicencia(models.Model):
    TIPO_DOC = [
        ("FACTURA", "Factura"),
        ("BOLETA", "Boleta"),
        ("OC", "Orden de Compra"),
        ("OTRO", "Otro"),
    ]

    llave = models.ForeignKey(LlaveLicencia, on_delete=models.CASCADE, related_name="historial")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento_nueva = models.DateField()
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOC)
    numero_documento = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.llave.numero_serie} - {self.tipo_documento} {self.numero_documento}"
