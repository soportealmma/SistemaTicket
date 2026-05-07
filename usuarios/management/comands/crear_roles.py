from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = "Crea grupos y permisos predeterminados"

    def handle(self, *args, **kwargs):
        roles = ['Administrador', 'Cliente', 'Integrador', 'Vendedor']

        for rol in roles:
            grupo, creado = Group.objects.get_or_create(name=rol)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Grupo creado: {rol}"))

        # Ejemplo: asignar permisos a Administrador
        admin_group = Group.objects.get(name='Administrador')
        permisos = Permission.objects.all()
        admin_group.permissions.set(permisos)

        self.stdout.write(self.style.SUCCESS("Roles creados y permisos asignados"))
