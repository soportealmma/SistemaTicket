from django.db import models
from gestion_tickets.models import Fabricante
from gestion_tickets.models import Ticket
from django.utils import timezone
from django.db.models import Count

# Create your models here.





class CanalAtencion(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: Teléfono, WhatsApp, Email, Laboratorio
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# modelos definir SLA (Acuerdos de Nivel de Servicio)
class SLA(models.Model):

    tickets_fabricante = models.IntegerField(default=0, help_text="Número de tickets por Fabricante")
    tickets_integrador = models.IntegerField(default=0, help_text="Número de tickets por Integrador")
    tickets_tiempo_respuesta = models.IntegerField(default=0, help_text="Tiempo de respuesta en horas")
    tickets_tiempo_resolucion = models.IntegerField(default=0, help_text="Tiempo de resolución en horas")
    tickets_cumplimiento = models.FloatField(default=0.0, help_text="% de cumplimiento del SLA")
    tickets_no_cumplimiento = models.FloatField(default=0.0, help_text="% de incumplimiento del SLA")
    tickets_en_garantia = models.IntegerField(default=0, help_text="Número de tickets en garantía")
    tickets_fuera_garantia = models.IntegerField(default=0, help_text="Número de tickets fuera de garantía")



    def __str__(self):
        return f"SLA - Fabricante: {self.tickets_fabricante}, Integrador: {self.tickets_integrador}"
    
    #Calculos SLA
    def numero_tickets_por_fabricante(self):
        fab = Ticket.objects.values('fabricante').annotate(aggregate_function=count('id')).groupby('nombre')
        return Ticket.objects.values("fabricante").count()
        



#CÁLCULO Y METRICAS SLA

"""
En el dashboard SLA puedes medir varias cosas:

Tiempo de respuesta interno (según canal y criticidad).

Tiempo de resolución interno.

Tiempo de resolución con fabricante (cuando el ticket requiere escalar).

% de cumplimiento en cada uno.

Ejemplo de cálculo:

Ticket creado vía WhatsApp (criticidad “Alto” → respuesta ≤ 8h, resolución ≤ 48h).

Pero si involucra fabricante Mircom (resolución garantizada en 72h) → medir también ese SLA aparte.


"""
# VISUALIZACION DASHBOARD
"""
En tu sla_dashboard, podrías mostrar:

Cumplimiento por criticidad.

Cumplimiento por canal (qué tan rápido respondes en WhatsApp vs. email, etc.).

Cumplimiento por fabricante (comparar si tus proveedores cumplen).

Alertas tempranas (tickets que se están acercando al vencimiento SLA).

Un gráfico sugerido:

Heatmap criticidad vs canal.

Barras apiladas para fabricante (cumplidos vs vencidos).

"""