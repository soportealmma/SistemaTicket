from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F
from gestion_tickets.views import is_soporte_or_admin   
from django.utils import timezone
from gestion_tickets.models import Ticket
import plotly.express as px

# Create your views here.




# --- Panel de Reportes y Estadísticas (Dashboard) ---
#@login_required
#@user_passes_test(is_soporte_or_admin)
def views_dashboard(request):
    total_tickets = Ticket.objects.count()
    tickets_abiertos = Ticket.objects.filter(estado='abierto').count()
    tickets_en_progreso = Ticket.objects.filter(estado='en_progreso').count()
    tickets_cerrados = Ticket.objects.filter(estado='cerrado').count()

    # Tickets por fabricante
    tickets_por_fabricante = Ticket.objects.values('fabricante__nombre').annotate(count=Count('id')).order_by('-count')

    # Tickets vencidos (ejemplo simple, la lógica real de alertas sería más robusta)
    tickets_vencidos = Ticket.objects.filter(
        estado__in=['abierto', 'en_progreso', 'pendiente'],
        fecha_respuesta_esperada__lt=timezone.now()
    ).count()

    context = {
        'total_tickets': total_tickets,
        'tickets_abiertos': tickets_abiertos,
        'tickets_en_progreso': tickets_en_progreso,
        'tickets_cerrados': tickets_cerrados,
        'tickets_por_fabricante': tickets_por_fabricante,
        'tickets_vencidos': tickets_vencidos,
    }
    return render(request, 'gestion_tickets/dashboard.html', context)



def views_sla_dashboard(request):
    # ======================
    # Datos desde el modelo
    # ======================
    criticidad_qs = (
        Ticket.objects.values("criticidad")
        .annotate(total=Count("id"))
        .order_by("criticidad")
    )
    canal_qs = (
        Ticket.objects.values("canal__nombre")
        .annotate(total=Count("id"))
        .order_by("canal__nombre")
    )
    fabricante_qs = (
        Ticket.objects.values("fabricante__nombre")
        .annotate(total=Count("id"))
        .order_by("fabricante__nombre")
    )

    cumplidos = Ticket.objects.filter(
        fecha_cierre__isnull=False,
        fecha_cierre__lte=F("fecha_resolucion_esperada")
    ).count()
    
    vencidos = Ticket.objects.filter(
        fecha_cierre__isnull=False,
        fecha_cierre__gt=F("fecha_resolucion_esperada")
    ).count()

    # ======================
    # Gráficos con Plotly
    # ======================

    # Criticidad
    fig1 = px.pie(
        names=[c["criticidad"] or "Sin dato" for c in criticidad_qs],
        values=[c["total"] for c in criticidad_qs],
        title="Tickets por Criticidad"
    )
    criticidad_chart = fig1.to_html(full_html=False)

    # Canal
    fig2 = px.bar(
        x=[c["canal__nombre"] or "Sin canal" for c in canal_qs],
        y=[c["total"] for c in canal_qs],
        title="Tickets por Canal"
    )
    canal_chart = fig2.to_html(full_html=False)

    # Cumplimiento SLA
    fig3 = px.Figure(data=[
        px.Bar(name="Cumplidos", x=["SLA"], y=[cumplidos], marker_color="green"),
        px.Bar(name="Vencidos", x=["SLA"], y=[vencidos], marker_color="red"),
    ])
    fig3.update_layout(barmode="group", title="Cumplimiento SLA")
    cumplimiento_chart = fig3.to_html(full_html=False)

    # Fabricante
    fig4 = px.pie(
        names=[f["fabricante__nombre"] or "Sin fabricante" for f in fabricante_qs],
        values=[f["total"] for f in fabricante_qs],
        title="Tickets por Fabricante"
    )
    fabricante_chart = fig4.to_html(full_html=False)

    # Contexto
    context = {
        "criticidad_chart": criticidad_chart,
        "canal_chart": canal_chart,
        "cumplimiento_chart": cumplimiento_chart,
        "fabricante_chart": fabricante_chart,
    }
    return render(request, "sla_dashboard.html", context)
