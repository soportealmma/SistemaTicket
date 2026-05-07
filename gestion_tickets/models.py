from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from usuarios.models import Usuario_soporte




# Create your models here.



class Fabricante(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre





class Ticket(models.Model):
    ESTADOS = (
        ('abierto', 'Abierto'),
        ('en_progreso', 'En Progreso'),
        ('cerrado', 'Cerrado'),
        ('pendiente', 'Pendiente de Información'),
    )
    PRIORIDADES = (
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    )
    SERVICIOS = (
        ('reparación', 'Reparación'),
        ('pruebas', 'Pruebas'),
        ('garantía', 'Garantía'),
        ('armado', 'Armado'),
        ('diagnóstico', 'Diagnóstico'),
        ('otro', 'Otro'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asignado_a = models.ForeignKey(Usuario_soporte, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados', verbose_name="Asignado a")
    fabricante = models.ForeignKey(Fabricante, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fabricante")
    asunto = models.CharField(max_length=255)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='abierto')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='Baja')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    fecha_respuesta_esperada = models.DateTimeField(blank=True, null=True, verbose_name="Fecha Límite de Respuesta")
    fecha_cierre = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Cierre")
    tipo_servicio = models.CharField(max_length=30, choices=SERVICIOS, default='diagnostico', verbose_name="Tipo de Servicio")
    horas_respuesta = models.PositiveIntegerField()
    horas_resolucion = models.PositiveIntegerField()



    class Meta:
        ordering = ['-fecha_creacion'] # Ordenar tickets por fecha de creación descendente


    def __str__(self):
        return f"Ticket #{self.id}: {self.asunto} ({self.estado})"

    def cerrar_ticket(self):
        self.estado = 'cerrado'
        self.fecha_cierre = timezone.now()
        self.save()

    def horas_respuesta(self):
        if self.fecha_cierre and self.fecha_creacion:
            delta = self.fecha_cierre - self.fecha_creacion
            return delta.total_seconds() / 3600  # Convertir a horas
        return None
    
    def horas_resolucion(self):
        if self.fecha_cierre and self.fecha_creacion:
            delta = self.fecha_cierre - self.fecha_creacion
            return delta.total_seconds() / 3600  # Convertir a horas
        return None
    

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
