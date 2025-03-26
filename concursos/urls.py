from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_concursos, name='lista_concursos'),
]