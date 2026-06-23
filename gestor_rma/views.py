from urllib import request
from django.shortcuts import render
#from httpx import request
from weasyprint import HTML, CSS
from django.utils import timezone
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SolicitudRMA, ResolucionRMA, RMAImagen
from .forms import SolicitudRMAForm, ResolucionRMAForm  
from gestion_tickets.models import Ticket, TicketImagen
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import timedelta


#vistas finales
def crear_rma_desde_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    fecha_cierre = timezone.now()

    if request.method == "POST":
        form = SolicitudRMAForm(request.POST)

        if form.is_valid():
            rma = form.save(commit=False)
            rma.ticket_origen = ticket

            # Cambiar estado del ticket
            ticket.estado = "cerrado"
            ticket.fecha_cierre = fecha_cierre
            ticket.save()

            fecha_creacion = timezone.now()
            rma.fecha_creacion = fecha_creacion

            # Si es viernes o sábado → sumar 5 días
            if fecha_creacion.weekday() in (4, 5):
                rma.fecha_respuesta = fecha_creacion + timedelta(days=5)
            else:
                rma.fecha_respuesta = fecha_creacion + timedelta(hours=72)

            rma.save()

            # Procesar imágenes dinámicas
            for key in request.FILES:
                if key.startswith("imagen_"):
                    numero = key.split("_")[1]
                    imagen = request.FILES[key]
                    descripcion = request.POST.get(f"descripcion_{numero}", "")

                    RMAImagen.objects.create(
                        rma=rma,
                        imagen=imagen,
                        descripcion=descripcion
                    )

            return redirect("detalle_rma", rma_id=rma.id)

    else:
        form = SolicitudRMAForm(initial={
            "ticket_origen": ticket.id,
            "cliente": ticket.cliente,
            "rut_cliente": ticket.rut_cliente,
            "contacto": ticket.contacto,
            "correo": ticket.correo,
            "telefono": ticket.telefono,
            "direccion": ticket.direccion,
            "ciudad": ticket.ciudad,
            "tipo_equipo": ticket.tipo_equipo,
            "fabricante": ticket.fabricante,
            "modelo": ticket.modelo,
            "numero_serie": ticket.numero_serie,
            "descripcion_falla": ticket.descripcion_falla,
            "observaciones": ticket.observaciones,
            "tipo_documento": ticket.tipo_documento,
            "numero_documento": ticket.numero_documento,
            "en_garantia": ticket.en_garantia,
            "sellos_intactos": ticket.sellos_intactos,
            "accesorios_recibidos": ticket.accesorios_recibidos,
        })

    return render(request, "rma/crear_solicitud.html", {
        "form": form,
        "ticket": ticket
    })



def detalle_rma(request, rma_id):
    solicitud = get_object_or_404(SolicitudRMA, id=rma_id)
    imagenes = RMAImagen.objects.filter(rma=solicitud)

    # Si existe resolución, la traemos
    resolucion = getattr(solicitud, "resolucion", None)

    return render(request, "rma/detalle_rma.html", {
        "solicitud": solicitud,
        "imagenes": imagenes,
        "resolucion": resolucion,
    })


def crear_resolucion_desde_rma(request, rma_id):
    solicitud = get_object_or_404(SolicitudRMA, id=rma_id)

    if hasattr(solicitud, "resolucion"):
        return redirect("detalle_resolucion_rma", resolucion_id=solicitud.resolucion.id)

    if request.method == "POST":
        form = ResolucionRMAForm(request.POST)
        if form.is_valid():
            resolucion = form.save(commit=False)
            resolucion.solicitud = solicitud
            resolucion.save()

            # 🔥 CERRAR LA SOLICITUD RMA
            solicitud.estado = "cerrado"      # Asegúrate que este valor exista en tu modelo
            solicitud.fecha_cierre = timezone.now()
            solicitud.save()
            messages.success(request="Resolución RMA generada con Exito!")
            return redirect("detalle_resolucion_rma", resolucion_id=resolucion.id)

    else:
        form = ResolucionRMAForm()

    return render(request, "rma/crear_resolucion.html", {
        "form": form,
        "solicitud": solicitud
    })


def detalle_resolucion_rma(request, resolucion_id):
    resolucion = get_object_or_404(ResolucionRMA, id=resolucion_id)
    return render(request, "rma/detalle_resolucion.html", {
        "resolucion": resolucion,
        "solicitud": resolucion.solicitud,

    })



def editar_resolucion_rma(request, resolucion_id):
    resolucion = get_object_or_404(ResolucionRMA, id=resolucion_id)
    rma = resolucion.solicitud  # acceso directo a la solicitud

    if request.method == "POST":
        form = ResolucionRMAForm(request.POST, instance=resolucion)
        nuevas_imagenes = request.FILES.getlist("imagenes")

        if form.is_valid():
            form.save()

            # Guardar nuevas imágenes si se subieron
            for img in nuevas_imagenes:
                RMAImagen.objects.create(
                    rma=rma,
                    imagen=img,
                    descripcion=f"Imagen añadida en edición de {resolucion.numero_resolucion}"
                )

            messages.success(request, "Resolución actualizada correctamente.")
            return redirect("detalle_resolucion_rma", resolucion_id=resolucion.id)

    else:
        form = ResolucionRMAForm(instance=resolucion)

    return render(request, "rma/editar_resolucion.html", {
        "form": form,
        "resolucion": resolucion,
        "solicitud": rma,
    })


def listar_resolucion(request):
    resoluciones = ResolucionRMA.objects.select_related("solicitud").order_by("-id")

    return render(request, "rma/listar_resolucion.html", {
        "resoluciones": resoluciones
    })


def editar_solicitud_rma(request, rma_id):
    solicitud = get_object_or_404(SolicitudRMA, id=rma_id)
    imagenes = solicitud.imagenes.all()  # related_name="imagenes"

    if request.method == "POST":
        form = SolicitudRMAForm(request.POST, instance=solicitud)

        if form.is_valid():
            form.save()

            # Procesar nuevas imágenes dinámicas
            for key in request.FILES:
                if key.startswith("imagen_"):
                    numero = key.split("_")[1]
                    imagen = request.FILES[key]
                    descripcion = request.POST.get(f"descripcion_{numero}", "")

                    RMAImagen.objects.create(
                        rma=solicitud,
                        imagen=imagen,
                        descripcion=descripcion
                    )

            return redirect("detalle_rma", rma_id=solicitud.id)

    else:
        form = SolicitudRMAForm(instance=solicitud)

    return render(request, "rma/editar_solicitud_rma.html", {
        "form": form,
        "solicitud": solicitud,
        "imagenes": imagenes,
    })


def eliminar_imagen_rma(request, imagen_id):
    imagen = get_object_or_404(RMAImagen, id=imagen_id)
    rma_id = imagen.rma.id
    imagen.delete()
    return redirect("editar_solicitud_rma", rma_id=rma_id)






#-----------Views RMA------------------

def crear_solicitud_rma(request):
    if request.method == 'POST':
        form = SolicitudRMAForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario_solicita = request.user
            solicitud.save()
            messages.success(request, "Solicitud RMA creada correctamente.")
        return redirect('listar_rma')
    else: 
        form = SolicitudRMAForm()
        messages.error(request, "Error al crear la solicitud RMA. Por favor, revisa los datos ingresados.")

    return render(request, 'rma/crear_solicitud.html', {'form': form})



def detalle_resolucion_rma(request, resolucion_id):
    resolucion = get_object_or_404(ResolucionRMA, id=resolucion_id)
    return render(request, "rma/detalle.html", {
        "resolucion": resolucion,
        "solicitud": resolucion.solicitud
    })


def listar_rma(request):
    rmas = SolicitudRMA.objects.all().order_by('-fecha_creacion')
    return render(request, 'rma/listar.html', {'rmas': rmas})



def exportar_rma_pdf(request, rma_id):
    solicitud = get_object_or_404(SolicitudRMA, pk=rma_id)
    resolucion = ResolucionRMA.objects.filter(solicitud=solicitud).first()
    username = request.user

    # CORRECCIÓN IMPORTANTE
    imagenes = RMAImagen.objects.filter(rma=solicitud)

    html_string = render_to_string("rma/pdf_rma.html", {
        "solicitud": solicitud,
        "resolucion": resolucion,
        "username": username,
        "lastname": request.user.last_name,
        "request": request,
        "imagenes": imagenes,
    })

    pdf_file = BytesIO()

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        target=pdf_file
    )

    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="RMA-{solicitud.id}.pdf"'
    return response
