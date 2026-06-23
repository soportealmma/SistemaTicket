from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from mantenedor.models import cliente, Fabricante, Localidad
from gestion_tickets.models import Ticket
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db import models





#-----------RMA-------------
class SolicitudRMA(models.Model):
    ticket_origen = models.OneToOneField(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name="rma" )
    numero_rma = models.CharField(max_length=50, blank=True)
    # ============================
    # A. Datos del Cliente
    # ============================
    cliente = models.ForeignKey(cliente, on_delete=models.SET_NULL, null=True, related_name="rmas")
    rut_cliente = models.CharField(max_length=20)
    contacto = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    ciudad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)

    # ============================
    # B. Datos Comerciales
    # ============================
    CHOICES_TIPO_DOCUMENTO = [
            ("factura", "Factura"),
            ("nota_venta", "Nota de Venta"),
            ("otro", "Otro"),
        ]
    CHOICES_ESTADO = [
        ('abierto','Abierto'),
        ('en_revision','En Revisión'),
        ('diagnosticado','Diagnosticado'),
        ('cerrado','Cerrado'),
    ]
    tipo_documento = models.CharField(choices=CHOICES_TIPO_DOCUMENTO,max_length=50, blank=True)
    numero_documento = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=CHOICES_ESTADO, default='abierto')
    en_garantia = models.BooleanField(default=False)

    # ============================
    # C. Datos Técnicos
    # ============================
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    tipo_equipo = models.CharField(max_length=100, null=True, blank=True)
    numero_serie = models.CharField(max_length=100, null=True, blank=True)

    descripcion_falla = models.TextField(null=True, blank=True)
    sellos_intactos = models.CharField(max_length=10, choices=[('cerrado','Cerrado'),('abierto','Abierto'),('na','N/A')])
    accesorios_recibidos = models.CharField(max_length=10, choices=[('completo','Completo'),('incompleto','Incompleto'),('na','N/A')])
    observaciones = models.TextField(blank=True)

    # ============================
    # D. Métricas
    # ============================
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    

    def generar_numero_rma(self):
        if self.ticket_origen:
            return f"RMA-{timezone.now().strftime('%y%m')}-{self.ticket_origen.id:06d}"
        return f"RMA-{timezone.now().strftime('%y%m')}-{self.ticket_origen.id:06d}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.numero_rma:
            self.numero_rma = self.generar_numero_rma()
            super().save(update_fields=["numero_rma"])

    def __str__(self):
        return f"RMA {self.id} - {self.cliente}"

        
from PIL import Image, ImageOps
from django.db import models

class RMAImagen(models.Model):
    rma = models.ForeignKey("SolicitudRMA", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="rma/")
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.imagen.path)

        # Convertir a RGB si es PNG o tiene canal alfa
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Recortar bordes blancos automáticamente (opcional)
        img = ImageOps.crop(img, border=5)

        # Redimensionar a tamaño web
        max_width = 900
        max_height = 900
        img.thumbnail((max_width, max_height), Image.LANCZOS)

        # Guardar optimizada
        img.save(self.imagen.path, format="JPEG", quality=85)


    def __str__(self):
        return f"Imagen RMA {self.rma.id}"


class ResolucionRMA(models.Model):
    solicitud = models.OneToOneField(SolicitudRMA, related_name="resolucion", on_delete=models.CASCADE)
    numero_resolucion = models.CharField(max_length=50, null=True, blank=True)
    ingeniero_responsable = models.CharField(max_length=200)
    condicion_fisica = models.CharField(max_length=20, choices=[('bueno','Bueno'), ('regular','Regular'), ('dañado','Dañado')])
    sellos_intactos = models.CharField(max_length=10, choices=[('cerrado','Cerrado'),('abierto','Abierto'),('na','N/A')])
    accesorios_recibidos = models.CharField(max_length=10, choices=[('completo','Completo'),('incompleto','Incompleto'),('na','N/A')])
    # ---- ANALISIS TÉCNICO ----
    descripcion_falla = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)
    diagnostico = models.CharField(max_length=200)
    causa_raiz = models.CharField(max_length=255, blank=True)
    rma_imagen = models.ForeignKey("RMAImagen", on_delete=models.SET_NULL, null=True, blank=True)
    aplica_garantia = models.CharField(max_length=200, choices=[('aprobado','Aprobado'), ('rechazada','Rechazada'), ('rma_fabrica','RMA a Fábrica'), ('no_aplica','No Aplica')])
    motivo_no_garantia = models.TextField(blank=True)
    fecha_cierre = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        creando = self.pk is None
        super().save(*args, **kwargs)

        if creando and not self.numero_resolucion:
            self.numero_resolucion = f"R-{timezone.now().strftime('%y%m')}-{self.solicitud.numero_rma}-{self.id}"
            super().save(update_fields=["numero_resolucion"])

    def __str__(self):
        return f"Resolución RMA {self.solicitud.id}"



