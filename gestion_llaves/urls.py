# gestion_llaves/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("listar/", views.listar_llaves, name="listar_llaves"),
    path("crear/", views.registrar_llave, name="crear_llave"),
    path("pdf/<int:pk>/", views.pdf_llave, name="pdf_llave"),
]
