from django.db import models
from django.contrib.auth.models import User, Group



class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.grupo.name if self.grupo else 'Sin grupo'}"



class Usuario_soporte(models.Model):
    user_soporte = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user_soporte.username} - Soporte Técnico"

    class Meta:
        verbose_name = "Usuario de Soporte"
        verbose_name_plural = "Usuarios de Soporte"