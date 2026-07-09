from django.urls import path
from .views import listar_usuarios, crear_usuario, editar_usuario, cambiar_estado_usuario, eliminar_usuario, dashboard_mantenedor


urlpatterns = [
    path("", listar_usuarios, name="listar_usuarios"),
    path("crear/", crear_usuario, name="crear_usuario"),
    path("editar/<int:user_id>/", editar_usuario, name="editar_usuario"),
    path("estado/<int:user_id>/", cambiar_estado_usuario, name="cambiar_estado_usuario"),
    path("eliminar/<int:user_id>/", eliminar_usuario, name="eliminar_usuario"),
    path("mantenedor/", dashboard_mantenedor, name="dashboard_mantenedor"),

]
