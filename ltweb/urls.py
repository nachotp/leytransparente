from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path(r'ley', views.SubirLeyView.as_view(), name='Subir Ley'),
    path(r'leyes', views.LeyesListView.as_view(), name='Lista Leyes'),
    path(r'declaracion/', views.SubirDeclaracionView.as_view(), name='Subir declaracion'),
    path(r'diputados/', views.DiputadosListView.as_view(), name='Lista Diputados'),
    path(r'ver/', views.EditarDeclaracion.as_view(), name='Ver Declaracion'),
    path(r'conflicto/<str:ley>', views.ConflictoView.as_view(), name='Conflictos')
]