from django.urls import path
from .views import createUsuario, updateUsuario, deleteUsuario, listUsuarios, login_view



urlpatterns = [
    #path('login/', login_view, name='login'),  # Asegúrate de que la vista login_view esté importada correctamente
    path('CrearUsuarios', createUsuario, name='crear_usuario'),
    #path('actualizar/<int:pk>/', updateUsuario, name='actualizar_usuario'),
    #path('eliminar/<int:pk>/', deleteUsuario, name='eliminar_usuario'),
    path('listarUsuarios/', listUsuarios, name='listar_usuarios'),  
]