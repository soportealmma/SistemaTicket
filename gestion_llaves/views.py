from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML, CSS
from io import BytesIO
import tempfile
import os
from .models import LlaveLicencia, HistorialLicencia
from .forms import RegistroLlaveForm




def listar_llaves(request):
   llaves = LlaveLicencia.objects.all().order_by("-fecha_registro")
   return render(request, "gestion_llaves/listar_llaves.html", {"llaves": llaves})

def buscar_llaves(request):
    q = request.GET.get("q", "")
    llaves = LlaveLicencia.objects.filter(numero_serie__iexact=q)

    if q:
        llaves = llaves.filter(
            models.Q(cliente__icontains=q) |
            models.Q(numero_serie__icontains=q) |
            models.Q(rut__icontains=q)
        )

    return render(request, "gestion_llaves/listar_llaves.html", {"llaves": llaves, "q": q})

def registrar_llave(request):
    q = request.GET.get("q", "").strip()
    llave = None
    coincidencias = []

    if q:
        coincidencias = LlaveLicencia.objects.filter(numero_serie__icontains=q)

        # Si hay exactamente 1 coincidencia → cargarla en el formulario
        if coincidencias.count() == 1:
            llave = coincidencias.first()

        # Si hay más de 1 → mostrar lista y NO cargar formulario aún
        elif coincidencias.count() > 1:
            return render(request, "gestion_llaves/seleccionar_llave.html", {
                "coincidencias": coincidencias,
                "q": q,
            })

    # Si viene selección desde la lista
    seleccion_id = request.GET.get("seleccion")
    if seleccion_id:
        llave = LlaveLicencia.objects.get(id=seleccion_id)

    # Procesar formulario
    if request.method == "POST":
        form = RegistroLlaveForm(request.POST, instance=llave)
        if form.is_valid():
            form.save()
            return redirect("listar_llaves")
    else:
        form = RegistroLlaveForm(instance=llave)

    return render(request, "gestion_llaves/registrar_llave.html", {
        "form": form,
        "llave": llave,
        "q": q,
    })


def editar_llave(request, pk):
    llave = get_object_or_404(LlaveLicencia, pk=pk)

    if request.method == "POST":
        form = RegistroLlaveForm(request.POST, instance=llave)
        if form.is_valid():
            form.save()
            return redirect("listar_llaves")
    else:
        form = RegistroLlaveForm(instance=llave)

    return render(request, "gestion_llaves/editar_llave.html", {"form": form, "llave": llave})


def pdf_llave(request, pk):
    llave = get_object_or_404(LlaveLicencia, pk=pk)

    html_string = render_to_string("gestion_llaves/pdf_llave.html", {
        "llave": llave,
        "username": request.user,
        "lastname": request.user.last_name,
    })

    pdf_file = BytesIO()

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        target=pdf_file,
        stylesheets=[CSS(string=""" 
            @page { size: A4; margin: 20mm; }
            body { font-family: sans-serif; font-size: 12px; }
            h1, h2, h3 { color: #333; }
            .section-title { font-size: 16px; font-weight: bold; margin-top: 10px; }
            .label { font-weight: bold; }
            .box { border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        """)]
    )

    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=Llave_{llave.numero_serie}.pdf"
    return response
