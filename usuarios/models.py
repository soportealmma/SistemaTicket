from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Perfil(models.Model):
    user = models.OneToOneField("usuarios.Usuario", on_delete=models.CASCADE)

    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to="usuarios/fotos/", blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)

    # Opcionales recomendados
    direccion = models.CharField(max_length=255, blank=True, null=True)
    comuna = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    estado_cuenta = models.BooleanField(default=True)  # Activo / Inactivo

    def __str__(self):
        return f"{self.user.email} - {self.rut}"
