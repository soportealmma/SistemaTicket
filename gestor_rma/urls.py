from django.urls import path
from .views import (crear_rma_desde_ticket, crear_solicitud_rma, crear_resolucion_desde_rma, 
                    detalle_resolucion_rma, exportar_rma_pdf, listar_rma, detalle_rma, listar_resolucion,
                    editar_solicitud_rma, eliminar_imagen_rma
)


urlpatterns = [
    #crear solicitud RMA
    path("crear-solicitud/", crear_solicitud_rma, name="crear_solicitud_rma"),
    # Crear RMA desde Ticket
    path("ticket/<int:id>/crear-rma/", crear_rma_desde_ticket, name="crear_rma_desde_ticket"),

    # Detalle RMA
    path("rma/<int:rma_id>/detalle/", detalle_rma, name="detalle_rma"),

    # Crear Resolución desde RMA
    path("rma/<int:rma_id>/crear-resolucion/", crear_resolucion_desde_rma, name="crear_resolucion_desde_rma"),

    # Detalle Resolución
    path("resolucion/<int:resolucion_id>/detalle/", detalle_resolucion_rma, name="detalle_resolucion_rma"),

    # Listados
    path("rma/listar/", listar_rma, name="listar_rma"),
    path("resoluciones/listar/", listar_resolucion, name="listar_resolucion"),

    # PDF
    path("rma/<int:rma_id>/pdf/", exportar_rma_pdf, name="exportar_rma_pdf"),

    # Editar solicitud RMA
    path("rma/<int:rma_id>/editar/", editar_solicitud_rma, name="editar_solicitud_rma"),

    # Eliminar imagen
    path("rma/imagen/<int:imagen_id>/eliminar/", eliminar_imagen_rma, name="eliminar_imagen_rma"),

]
