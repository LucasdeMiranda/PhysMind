from django.urls import path
from .views import CriaUsuario

urlpatterns = [
    path('cria-usuario/', CriaUsuario.as_view()),
]
