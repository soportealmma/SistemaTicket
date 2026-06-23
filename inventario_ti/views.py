from django.shortcuts import render, redirect, get_object_or_404
from .models import EquipoTI, CelularTI, LicenciaTI, HistorialAsignacion
from .forms import EquipoTIForm, CelularTIForm, LicenciaTIForm, AsignacionForm, DevolucionForm
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os
from .models import DocumentoEntrega, EquipoTI, CelularTI, LicenciaTI
from django.contrib.auth.models import User
from datetime import date




# ============================
# LISTADO DE EQUIPOS
# ============================
def listar_equipos(request):
    equipos = EquipoTI.objects.all().order_by("tipo_equipo", "marca")
    return render(request, "inventario_ti/listar_equipos.html", {"equipos": equipos})


# ============================
# CREAR EQUIPO
# ============================
def crear_equipo(request):
    if request.method == "POST":
        form = EquipoTIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_equipos")
    else:
        form = EquipoTIForm()

    return render(request, "inventario_ti/crear_equipo.html", {"form": form})


# ============================
# EDITAR EQUIPO
# ============================
def editar_equipo(request, pk):
    equipo = get_object_or_404(EquipoTI, pk=pk)

    if request.method == "POST":
        form = EquipoTIForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect("listar_equipos")
    else:
        form = EquipoTIForm(instance=equipo)

    return render(request, "inventario_ti/editar_equipo.html", {"form": form, "equipo": equipo})


# ============================
# ELIMINAR EQUIPO
# ============================
def eliminar_equipo(request, pk):
    equipo = get_object_or_404(EquipoTI, pk=pk)
    equipo.delete()
    return redirect("listar_equipos")



# ============================
# LISTADO CELULARES
# ============================
def listar_celulares(request):
    celulares = CelularTI.objects.all().order_by("marca", "modelo")
    return render(request, "inventario_ti/listar_celulares.html", {"celulares": celulares})

def crear_celular(request):
    if request.method == "POST":
        form = CelularTIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_celulares")
    else:
        form = CelularTIForm()
    return render(request, "inventario_ti/crear_celular.html", {"form": form})

def editar_celular(request, pk):
    celular = get_object_or_404(CelularTI, pk=pk)
    if request.method == "POST":
        form = CelularTIForm(request.POST, instance=celular)
        if form.is_valid():
            form.save()
            return redirect("listar_celulares")
    else:
        form = CelularTIForm(instance=celular)
    return render(request, "inventario_ti/editar_celular.html", {"form": form, "celular": celular})

def eliminar_celular(request, pk):
    celular = get_object_or_404(CelularTI, pk=pk)
    celular.delete()
    return redirect("listar_celulares")


# ============================
# LISTADO LICENCIAS
# ============================
def listar_licencias(request):
    licencias = LicenciaTI.objects.all().order_by("tipo_licencia", "producto")
    return render(request, "inventario_ti/listar_licencias.html", {"licencias": licencias})

def crear_licencia(request):
    if request.method == "POST":
        form = LicenciaTIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("listar_licencias")
    else:
        form = LicenciaTIForm()
    return render(request, "inventario_ti/crear_licencia.html", {"form": form})

def editar_licencia(request, pk):
    licencia = get_object_or_404(LicenciaTI, pk=pk)
    if request.method == "POST":
        form = LicenciaTIForm(request.POST, instance=licencia)
        if form.is_valid():
            form.save()
            return redirect("listar_licencias")
    else:
        form = LicenciaTIForm(instance=licencia)
    return render(request, "inventario_ti/editar_licencia.html", {"form": form, "licencia": licencia})

def eliminar_licencia(request, pk):
    licencia = get_object_or_404(LicenciaTI, pk=pk)
    licencia.delete()
    return redirect("listar_licencias")





# ============================
# LISTADO DE ASIGNACIONES
# ============================
def listar_asignaciones(request):
    asignaciones = HistorialAsignacion.objects.order_by("-fecha_inicio")
    return render(request, "inventario_ti/listar_asignaciones.html", {"asignaciones": asignaciones})


# ============================
# CREAR ASIGNACIÓN
# ============================
def crear_asignacion(request):
    if request.method == "POST":
        form = AsignacionForm(request.POST)
        if form.is_valid():
            asignacion = form.save()

            # Actualizar responsable actual
            if asignacion.equipo:
                asignacion.equipo.responsable_actual = asignacion.persona
                asignacion.equipo.save()

            if asignacion.celular:
                asignacion.celular.responsable_actual = asignacion.persona
                asignacion.celular.save()

            if asignacion.licencia:
                asignacion.licencia.responsable_actual = asignacion.persona
                asignacion.licencia.save()

            messages.success(request, "Asignación registrada correctamente.")
            return redirect("listar_asignaciones")
    else:
        form = AsignacionForm()

    return render(request, "inventario_ti/crear_asignacion.html", {"form": form})


# ============================
# CERRAR / TERMINAR ASIGNACIÓN
# ============================
def cerrar_asignacion(request, pk):
    asignacion = get_object_or_404(HistorialAsignacion, pk=pk)

    if request.method == "POST":
        form = AsignacionForm(request.POST, instance=asignacion)
        if form.is_valid():
            asignacion = form.save()

            # Liberar responsable actual
            if asignacion.equipo:
                asignacion.equipo.responsable_actual = None
                asignacion.equipo.save()

            if asignacion.celular:
                asignacion.celular.responsable_actual = None
                asignacion.celular.save()

            if asignacion.licencia:
                asignacion.licencia.responsable_actual = None
                asignacion.licencia.save()

            messages.success(request, "Asignación cerrada correctamente.")
            return redirect("listar_asignaciones")
    else:
        form = AsignacionForm(instance=asignacion)

    return render(request, "inventario_ti/cerrar_asignacion.html", {"form": form, "asignacion": asignacion})


def ver_asignacion(request, pk):
    asignacion = get_object_or_404(HistorialAsignacion, pk=pk)
    return render(request, "inventario_ti/ver_asignacion.html", {"asignacion": asignacion})



def editar_asignacion(request, pk):
    asignacion = get_object_or_404(HistorialAsignacion, pk=pk)

    if request.method == "POST":
        form = AsignacionForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()

            # Actualizar responsable_actual si cambió
            if asignacion.equipo:
                asignacion.equipo.responsable_actual = asignacion.persona
                asignacion.equipo.save()

            if asignacion.celular:
                asignacion.celular.responsable_actual = asignacion.persona
                asignacion.celular.save()

            if asignacion.licencia:
                asignacion.licencia.responsable_actual = asignacion.persona
                asignacion.licencia.save()

            return redirect("listar_asignaciones")
    else:
        form = AsignacionForm(instance=asignacion)

    return render(request, "inventario_ti/editar_asignacion.html", {
        "form": form,
        "asignacion": asignacion
    })




#=================
#-----PDF--------#
#=================

def generar_documento_entrega(request, user_id):

    persona = get_object_or_404(User, pk=user_id)

    equipos = EquipoTI.objects.filter(responsable_actual=persona)
    celulares = CelularTI.objects.filter(responsable_actual=persona)
    licencias = LicenciaTI.objects.filter(responsable_actual=persona)

    # Render HTML
    html_string = render_to_string("inventario_ti/documento_entrega.html", {
        "persona": persona,
        "equipos": equipos,
        "celulares": celulares,
        "licencias": licencias,
        "fecha": date.today(),
    })

    # Crear PDF en memoria
    pdf_file = HTML(string=html_string).write_pdf(
        stylesheets=[CSS(string="""
            @page { size: Letter; margin: 2cm; }
            body { font-family: Arial, sans-serif; font-size: 12px; }
            h1, h2, h3 { color: #0d6efd; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { border: 1px solid #ccc; padding: 6px; }
            th { background: #f0f0f0; }
            .firma { margin-top: 60px; text-align: center; }
        """)]
    )

    # Respuesta HTTP
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=entrega_{persona.username}.pdf"

    return response




def generar_pdf_recepcion(request, user_id):
    persona = get_object_or_404(User, pk=user_id)

    # Devoluciones registradas para esta persona (puedes ajustar el filtro según tu lógica)
    devoluciones = HistorialAsignacion.objects.filter(
        persona=persona,
        fecha_termino__isnull=False
    ).order_by("-fecha_termino")

    html_string = render_to_string("inventario_ti/documento_recepcion.html", {
        "persona": persona,
        "devoluciones": devoluciones,
        "fecha": date.today(),
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=recepcion_{persona.username}.pdf"

    return response


#===========================
#---CREA VISTA PARA MODAL---
#===========================

def seleccionar_devolucion(request, asignacion_id):
    asignacion = get_object_or_404(HistorialAsignacion, pk=asignacion_id)
    persona = asignacion.persona

    # Equipos actualmente asignados a esta persona
    equipos = EquipoTI.objects.filter(responsable_actual=persona)
    celulares = CelularTI.objects.filter(responsable_actual=persona)
    licencias = LicenciaTI.objects.filter(responsable_actual=persona)

    form = DevolucionForm()
    form.fields["equipos"].queryset = equipos
    form.fields["celulares"].queryset = celulares
    form.fields["licencias"].queryset = licencias

    return render(request, "inventario_ti/devolucion_modal.html", {
        "form": form,
        "asignacion": asignacion,
    })


def procesar_devolucion(request, asignacion_id):
    asignacion = get_object_or_404(HistorialAsignacion, pk=asignacion_id)
    persona = asignacion.persona

    if request.method != "POST":
        return redirect("listar_asignaciones")

    form = DevolucionForm(request.POST)
    form.fields["equipos"].queryset = EquipoTI.objects.filter(responsable_actual=persona)
    form.fields["celulares"].queryset = CelularTI.objects.filter(responsable_actual=persona)
    form.fields["licencias"].queryset = LicenciaTI.objects.filter(responsable_actual=persona)

    if not form.is_valid():
        return redirect("listar_asignaciones")

    equipos = form.cleaned_data["equipos"]
    celulares = form.cleaned_data["celulares"]
    licencias = form.cleaned_data["licencias"]
    motivo = form.cleaned_data["motivo"]
    observaciones = form.cleaned_data["observaciones"]

    # Procesar devoluciones
    for e in equipos:
        HistorialAsignacion.objects.create(
            persona=persona,
            equipo=e,
            fecha_inicio=asignacion.fecha_inicio,
            fecha_termino=date.today(),
            motivo_termino=motivo,
            observaciones=observaciones,
        )
        e.responsable_actual = None
        e.save()

    for c in celulares:
        HistorialAsignacion.objects.create(
            persona=persona,
            celular=c,
            fecha_inicio=asignacion.fecha_inicio,
            fecha_termino=date.today(),
            motivo_termino=motivo,
            observaciones=observaciones,
        )
        c.responsable_actual = None
        c.save()

    for l in licencias:
        HistorialAsignacion.objects.create(
            persona=persona,
            licencia=l,
            fecha_inicio=asignacion.fecha_inicio,
            fecha_termino=date.today(),
            motivo_termino=motivo,
            observaciones=observaciones,
        )
        l.responsable_actual = None
        l.save()

    # Redirigir a PDF de recepción
    return redirect("generar_pdf_recepcion", user_id=persona.id)


