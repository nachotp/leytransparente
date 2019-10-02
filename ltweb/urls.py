from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path(r'ley', views.SubirLeyView.as_view(), name='Subir Ley'),
    path(r'leyes', login_required(views.LeyesListView.as_view()), name='Lista Leyes'),
    path(r'declaracion/', views.SubirDeclaracionView.as_view(), name='Subir declaracion'),
    path(r'diputados/', login_required(views.DiputadosListView.as_view()), name='Lista Diputados'),
    path(r'ver/<str:id>', login_required(views.ViewDeclaracion.as_view()), name='Ver Declaracion'),
    path(r'conflicto/<str:ley>', views.ConflictoView.as_view(), name='Conflictos'),
    path(r'conflictos', login_required(views.ConflictoListView.as_view()), name='Lista Conflictos'),
    path(r'registro', views.RegistroView.as_view(), name='Registro de usuario'),
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'logout/', LogoutView.as_view(), name='logout'),
    path(r'control/', views.ControlView.as_view(), name='Control de usuario'),
    path(r'cluster/', views.ClusterView.as_view(), name='Cluster'),
    path(r'actualizar/<str:id>', views.ActualizarView.as_view(), name='Actualizar Usuario'),
    path(r'actualizar_permisos/', views.ActualizarPermisosView.as_view(), name='Actualizar Permisos'),
    path(r'eliminar_usuario/<str:id>', views.EliminarUserView.as_view(), name='Eliminar Usuario')
]