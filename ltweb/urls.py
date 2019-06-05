from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='Home'),
    path(r'Declaracion/', views.SubirDeclaracionView.as_view(), name='Subir declaracion'),
    path(r'Editar/', views.EditarDeclaracion.as_view(), name='Editar Declaracion'),
    path(r'Diputados/', views.DiputadosListView.as_view(), name='Lista Diputados')
]