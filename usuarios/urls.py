from django.urls import path
from .views import CriaUsuario
from .views import  ObtemPerfil

urlpatterns = [
    path('cria-usuario/', CriaUsuario.as_view()),
    path('perfil/',ObtemPerfil.as_view()),
    
]
