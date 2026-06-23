from django.urls import path
from .views import home, crear_ticket, listar_tickets, detalle_ticket, editar_ticket, cerrar_ticket, abrir_ticket, exportar_ticket_pdf


urlpatterns = [
    path('home', home, name='home'),
    path('crearTicket', crear_ticket, name='crear_ticket'),
    path('listarTicket', listar_tickets, name='listar_ticket'),
    path('detalleTicket/<int:pk>', detalle_ticket, name='detalle_ticket'),
    path('editarTicket/<int:pk>', editar_ticket, name='editar_ticket'),
    path('cerrarTicket/<int:pk>', cerrar_ticket, name='cerrar_ticket'),
    path('abrirTicket/<int:pk>', abrir_ticket, name='abrir_ticket'),   
    path("ticket/<int:id>/pdf/", exportar_ticket_pdf, name="exportar_ticket_pdf"),


    
]

# Nota: Asegúrate de que las vistas y formularios importados existan y estén correctamente implementados.