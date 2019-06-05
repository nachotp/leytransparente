from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path(r'Ley', views.SubirLeyView.as_view(), name='Subir Ley'),
    path(r'Leyes', views.LeyesListView.as_view(), name='Lista Leyes'),
    path(r'Declaracion/', views.SubirDeclaracionView.as_view(), name='Subir declaracion'),
    path(r'Diputados/', views.DiputadosListView.as_view(), name='Lista Diputados'),
    path(r'Editar/', views.EditarDeclaracion.as_view(), name='Editar Declaracion')
]