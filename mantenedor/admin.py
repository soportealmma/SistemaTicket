from django.contrib import admin
from .models import Localidad, cliente, Fabricante

# Register your models here.


admin.site.register(Localidad)
admin.site.register(cliente)
admin.site.register(Fabricante)