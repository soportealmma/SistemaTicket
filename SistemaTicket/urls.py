from django.contrib import admin
from django.urls import path, include
from gestion_tickets.views import home
from django.contrib.auth import views as auth_views





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Redirigir a la vista de inicio
    path('', include('usuarios.urls')),
    path('', include('gestion_tickets.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   
]
