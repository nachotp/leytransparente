from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view()),
    path(r'Declaracion', views.SubirDeclaracion, name='Subir declaracion')
]