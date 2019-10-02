from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path(r'ley', views.SubirLeyView.as_view(), name='Subir Ley'),
    path(r'leyes', views.LeyesListView.as_view(), name='Lista Leyes'),
    path(r'declaracion/', views.SubirDeclaracionView.as_view(), name='Subir declaracion'),
    path(r'diputados/', views.DiputadosListView.as_view(), name='Lista Diputados'),
    path(r'ver/<str:id>', views.ViewDeclaracion.as_view(), name='Ver Declaracion'),
    path(r'conflicto/<str:ley>', views.ConflictoView.as_view(), name='Conflictos'),
    path(r'conflictos', views.ConflictoListView.as_view(), name='Lista Conflictos'),
    path(r'registro', views.RegistroView.as_view(), name='Registro de usuario'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    path(r'control/', views.ControlView.as_view(), name='Control de usuario'),
    path(r'cluster/', views.ClusterView.as_view(), name='Cluster'),
    path(r'actualizar/', views.ActualizarView.as_view(), name='Actualizar Usuario')
]