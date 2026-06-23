from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Tarea, TareaMensaje
from .forms import TareaForm, TareaMensajeForm
from django.contrib.auth.models import User
from django.db.models import Count, Avg, F
import json
from django.db.models.functions import TruncMonth
from datetime import timedelta
from datetime import datetime





def listar_tareas(request):
    tareas = Tarea.objects.all().order_by("-fecha_creacion")

    # Parámetros de filtro desde GET
    estado = request.GET.get("estado") or ""
    criticidad = request.GET.get("criticidad") or ""
    area = request.GET.get("area") or ""
    responsable_id = request.GET.get("responsable") or ""

    # Aplicar filtros
    if estado:
        tareas = tareas.filter(estado=estado)

    if criticidad:
        tareas = tareas.filter(criticidad=criticidad)

    if area:
        tareas = tareas.filter(area=area)

    if responsable_id:
        tareas = tareas.filter(responsable_id=responsable_id)

    form_crear = TareaForm()
    responsables = User.objects.all().order_by("first_name", "last_name")

    context = {
        "tareas": tareas,
        "form_crear": form_crear,
        "responsables": responsables,
        "ESTADOS": Tarea.ESTADOS,
        "CRITICIDADES": Tarea.CRITICIDAD,
        "AREAS": Tarea.AREAS,
        "filtros": {
            "estado": estado,
            "criticidad": criticidad,
            "area": area,
            "responsable": responsable_id,
        },
    }

    return render(request, "tareas/listar_tareas.html", context)



def crear_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.creado_por = request.user
            tarea.save()
            return redirect("listar_tareas")

    return redirect("listar_tareas")


def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    mensajes = tarea.mensajes.all()
    form_mensaje = TareaMensajeForm()

    return render(request, "tareas/detalle_tarea.html", {
        "tarea": tarea,
        "mensajes": mensajes,
        "form_mensaje": form_mensaje,
    })


def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == "POST":
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea = form.save()

            # Registrar fecha de cierre si se completó
            if tarea.estado == "completada" and not tarea.fecha_cierre:
                tarea.fecha_cierre = timezone.now()
                tarea.save()

            return redirect("detalle_tarea", tarea_id=tarea.id)

    form = TareaForm(instance=tarea)

    return render(request, "tareas/editar_tarea.html", {
        "form": form,
        "tarea": tarea,
    })


def agregar_mensaje_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    if request.method == "POST":
        form = TareaMensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.tarea = tarea
            mensaje.usuario = request.user
            mensaje.save()

    return redirect("detalle_tarea", tarea_id=tarea.id)


def cerrar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)

    tarea.estado = "completada"
    tarea.criticidad = "baja"  # criticidad mínima al cerrar
    tarea.fecha_cierre = timezone.now()
    tarea.save()

    # Registrar mensaje automático
    TareaMensaje.objects.create(
        tarea=tarea,
        usuario=request.user,
        mensaje="La tarea fue cerrada por el usuario."
    )

    return redirect("detalle_tarea", tarea_id=tarea.id)






def dashboard_tareas(request):

    # ============================
    # CAPTURA DE FILTROS
    # ============================
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    inicio = None
    fin = None

    if fecha_inicio:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

    if fecha_fin:
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    # Construcción del filtro dinámico
    filtro_fecha = {}

    if inicio and fin:
        filtro_fecha["fecha_creacion__date__range"] = [inicio, fin]
    elif inicio:
        filtro_fecha["fecha_creacion__date__gte"] = inicio
    elif fin:
        filtro_fecha["fecha_creacion__date__lte"] = fin

    # ============================
    # MÉTRICAS BÁSICAS
    # ============================
    tareas_por_estado = list(
        Tarea.objects.filter(**filtro_fecha)
        .values("estado")
        .annotate(total=Count("id"))
    )

    tareas_por_criticidad = list(
        Tarea.objects.filter(**filtro_fecha)
        .values("criticidad")
        .annotate(total=Count("id"))
    )

    tareas_por_area = list(
        Tarea.objects.filter(**filtro_fecha)
        .values("area")
        .annotate(total=Count("id"))
    )

    tareas_por_responsable = list(
        Tarea.objects.filter(**filtro_fecha)
        .values("responsable__first_name", "responsable__last_name")
        .annotate(total=Count("id"))
    )

    # ============================
    # TAREAS ATRASADAS
    # ============================
    atrasadas = [
        t for t in Tarea.objects.filter(**filtro_fecha)
        if t.esta_atrasada
    ]

    # ============================
    # TAREAS CREADAS POR MES
    # ============================
    creadas_raw = (
        Tarea.objects.filter(**filtro_fecha)
        .annotate(mes=TruncMonth("fecha_creacion"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )

    tareas_creadas_mes = [
        {"mes": item["mes"].strftime("%Y-%m-%d"), "total": item["total"]}
        for item in creadas_raw
    ]

    # ============================
    # TAREAS CERRADAS POR MES
    # ============================
    cerradas_raw = (
        Tarea.objects.filter(fecha_cierre__isnull=False)
        .filter(**filtro_fecha)
        .annotate(mes=TruncMonth("fecha_cierre"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )

    tareas_cerradas_mes = [
        {"mes": item["mes"].strftime("%Y-%m-%d"), "total": item["total"]}
        for item in cerradas_raw
    ]

    # ============================
    # TIEMPO PROMEDIO DE RESOLUCIÓN
    # ============================
    tareas_resueltas = Tarea.objects.filter(fecha_cierre__isnull=False).filter(**filtro_fecha)

    if tareas_resueltas.exists():
        tiempos = [
            (t.fecha_cierre - t.fecha_creacion).total_seconds() / 3600
            for t in tareas_resueltas
        ]
        tiempo_promedio_horas = round(sum(tiempos) / len(tiempos), 1)
    else:
        tiempo_promedio_horas = 0

    # ============================
    # TOP 5 RESPONSABLES
    # ============================
    ranking_responsables = list(
        Tarea.objects.filter(**filtro_fecha)
        .values("responsable__first_name", "responsable__last_name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    # ============================
    # CONTEXTO JSON SERIALIZABLE
    # ============================
    context = {
        "tareas_por_estado": json.dumps(tareas_por_estado),
        "tareas_por_criticidad": json.dumps(tareas_por_criticidad),
        "tareas_por_area": json.dumps(tareas_por_area),
        "tareas_por_responsable": json.dumps(tareas_por_responsable),
        "tareas_creadas_mes": json.dumps(tareas_creadas_mes),
        "tareas_cerradas_mes": json.dumps(tareas_cerradas_mes),
        "ranking_responsables": json.dumps(ranking_responsables),
        "tiempo_promedio_horas": tiempo_promedio_horas,
        "total_atrasadas": len(atrasadas),
    }

    return render(request, "tareas/dashboard_tareas.html", context)


