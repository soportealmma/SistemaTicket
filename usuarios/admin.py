from django.contrib import admin
from .models import  Perfil

# Register your models here.

admin.site.site_header = "Sistema de Tickets"
admin.site.site_title = "Administración de Tickets"
admin.site.register(Perfil)