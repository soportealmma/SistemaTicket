from django.urls import path
from .views import (listar_equipos, crear_equipo, editar_equipo, eliminar_equipo, 
listar_celulares, crear_celular, editar_celular, eliminar_celular, listar_licencias,
crear_licencia, editar_licencia, eliminar_licencia, listar_asignaciones, crear_asignacion, 
cerrar_asignacion, ver_asignacion, editar_asignacion, generar_documento_entrega,
seleccionar_devolucion, procesar_devolucion, generar_pdf_recepcion)



urlpatterns = [
    # Equipos
    path("equipos/", listar_equipos, name="listar_equipos"),
    path("equipos/crear/", crear_equipo, name="crear_equipo"),
    path("equipos/editar/<int:pk>/", editar_equipo, name="editar_equipo"),
    path("equipos/eliminar/<int:pk>/", eliminar_equipo, name="eliminar_equipo"),

    # Celulares
    path("celulares/", listar_celulares, name="listar_celulares"),
    path("celulares/crear/", crear_celular, name="crear_celular"),
    path("celulares/editar/<int:pk>/", editar_celular, name="editar_celular"),
    path("celulares/eliminar/<int:pk>/", eliminar_celular, name="eliminar_celular"),

    # Licencias
    path("licencias/", listar_licencias, name="listar_licencias"),
    path("licencias/crear/", crear_licencia, name="crear_licencia"),
    path("licencias/editar/<int:pk>/", editar_licencia, name="editar_licencia"),
    path("licencias/eliminar/<int:pk>/", eliminar_licencia, name="eliminar_licencia"),

    # Asignaciones
    path("asignaciones/", listar_asignaciones, name="listar_asignaciones"),
    path("asignaciones/crear/", crear_asignacion, name="crear_asignacion"),
    path("asignaciones/cerrar/<int:pk>/", cerrar_asignacion, name="cerrar_asignacion"),
    path("asignaciones/ver/<int:pk>/", ver_asignacion, name="ver_asignacion"),
    path("asignaciones/editar/<int:pk>/", editar_asignacion, name="editar_asignacion"),

    # Devolución parcial
    path("asignaciones/devolucion/<int:asignacion_id>/", seleccionar_devolucion, name="seleccionar_devolucion"),
    path("asignaciones/devolucion/procesar/<int:asignacion_id>/", procesar_devolucion, name="procesar_devolucion"),

    # GENERAR PDF
    path("asignaciones/generar-documento-entrega/<int:user_id>/", generar_documento_entrega, name="generar_documento_entrega"),
    path("recepcion/<int:user_id>/", generar_pdf_recepcion, name="generar_pdf_recepcion"),

]
