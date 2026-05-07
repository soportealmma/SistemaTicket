from django.contrib import admin
from .models import Usuario_soporte, Perfil

# Register your models here.

admin.site.site_header = "Sistema de Tickets"
admin.site.site_title = "Administración de Tickets"
admin.site.register(Usuario_soporte)
admin.site.register(Perfil)