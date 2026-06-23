from django.urls import path
from .views import listar_tareas, crear_tarea, detalle_tarea, editar_tarea, agregar_mensaje_tarea, cerrar_tarea, dashboard_tareas

urlpatterns = [
    path("tareas/", listar_tareas, name="listar_tareas"),
    path("tareas/crear/", crear_tarea, name="crear_tarea"),
    path("tareas/<int:tarea_id>/", detalle_tarea, name="detalle_tarea"),
    path("tareas/<int:tarea_id>/editar/", editar_tarea, name="editar_tarea"),
    path("tareas/<int:tarea_id>/mensaje/", agregar_mensaje_tarea, name="agregar_mensaje_tarea"),
    path("tareas/<int:tarea_id>/cerrar/", cerrar_tarea, name="cerrar_tarea"),
    path("tareas/dashboard/", dashboard_tareas, name="dashboard_tareas"),


]
