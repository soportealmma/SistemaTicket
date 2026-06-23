from .models import Ticket

def contador_tickets(request):
    if request.user.is_authenticated:
        pendientes = Ticket.objects.filter(estado='abierto').count()
    else:
        pendientes = 0

    return {'tickets_pendientes': pendientes}
