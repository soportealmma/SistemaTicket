from django.contrib import messages
from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tarea(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_progreso", "En progreso"),
        ("completada", "Completada"),
        ("atrasada", "Atrasada"),
    ]

    CRITICIDAD = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("critica", "Crítica"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_compromiso = models.DateField()
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    estado = models.CharField(max_length=20, choices=ESTADOS, default="Pendiente")
    criticidad = models.CharField(max_length=20, choices=CRITICIDAD, default="media")

    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tareas_asignadas"
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tareas_creadas"
    )

    observaciones = models.TextField(blank=True, null=True)

    AREAS = [
    ("soporte", "Soporte"),
    ("comercial", "Comercial"),
    ("operaciones", "Operaciones"),
    ("administracion", "Administración"),
    ("logistica", "Logística"),
    ("ti", "TI"),
    ("almmadigital", "AlmmaDigital"),
]

    area = models.CharField(max_length=30, choices=AREAS, default="soporte")


    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Tarea #{self.id} - {self.titulo}"

    @property
    def esta_atrasada(self):
        if self.estado != "completada" and self.fecha_compromiso < timezone.now().date():
            return True
        return False

    @property
    def color_criticidad(self):
        return {
            "baja": "success",
            "media": "warning",
            "alta": "orange",
            "critica": "danger",
        }.get(self.criticidad, "secondary")
    
    @property
    def color_estado(self):
        return {
            "pendiente": "warning",     # amarillo
            "en_progreso": "primary",   # azul
            "completada": "success",    # verde
            "atrasada": "danger",       # rojo
        }.get(self.estado, "warning")



class TareaMensaje(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="mensajes")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha"]

    def __str__(self):
        return f"Mensaje en Tarea #{self.tarea.id} por {self.usuario}"

