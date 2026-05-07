from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Perfil

User = get_user_model()

#@receiver(post_save, sender=User)
#def crear_perfil_y_asignar_grupo(sender, instance, created, **kwargs):
    #if created:
        #perfil = Perfil.objects.create(user=instance)
        # Asignar grupo Integrador por defecto
       # grupo_integrador, _ = Group.objects.get_or_create(name="Integrador")
       # perfil.grupo = grupo_integrador
       # perfil.save()



@receiver(post_save, sender=User)
def crear_perfil_y_asignar_grupo(sender, instance, created, **kwargs):
    if created:
        # Asignar grupo por defecto
        grupo_default, _ = Group.objects.get_or_create(name="Integrador")
        instance.groups.add(grupo_default)

        # Crear el perfil vinculado al usuario y grupo
        Perfil.objects.create(user=instance, grupo=grupo_default)