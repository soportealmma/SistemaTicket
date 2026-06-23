from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from usuarios.models import Usuario_soporte
from mantenedor.models import cliente, Fabricante, Localidad
from PIL import Image, ImageOps



# Create your models here.
class Ticket(models.Model):

    TIPO_DOCUMENTO_CHOICES = [
        ("factura", "Factura"),
        ("nota_venta", "Nota de Venta"),
        ("otro", "Otro"),
    ]

    ESTADO_CHOICES = [
        ("abierto", "Abierto"),
        ("pendiente", "Pendiente"),
        ("cerrado", "Cerrado"),
    ]

    # ============================
    # A. Datos del Cliente
    # ============================
    cliente = models.ForeignKey(cliente, on_delete=models.SET_NULL, null=True, related_name="tickets")
    rut_cliente = models.CharField(max_length=20)
    contacto = models.CharField(max_length=200)
    correo = models.EmailField(max_length=200)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    ciudad = models.ForeignKey(Localidad, on_delete=models.SET_NULL, null=True, blank=True)


    # ============================
    # B. Datos Comerciales
    # ============================
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default="factura")
    numero_documento = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="abierto")
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

    def __str__(self):
        return f"Ticket {self.id}"

    

class Mensaje(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='mensajes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    es_respuesta = models.BooleanField(default=True, verbose_name="¿Es una respuesta?") # Para diferenciar preguntas iniciales de respuestas

    class Meta:
        ordering = ['fecha_envio'] # Ordenar mensajes cronológicamente

    def __str__(self):
        return f"Mensaje de {self.usuario} en Ticket #{self.ticket.id}"




class TicketImagen(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="tickets/", null=True, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

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
        return f"Imagen Ticket {self.ticket.id}"


