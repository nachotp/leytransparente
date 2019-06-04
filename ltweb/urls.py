from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view()),
    path(r'Declaracion', views.SubirDeclaracionView.as_view(), name='Subir declaracion')
]