from django.urls import path
from .views import CriaUsuario
from .views import  PerfilView
from rest_framework_simplejwt.views import(
    TokenRefreshView
)

urlpatterns = [
    path('cria-usuario/', CriaUsuario.as_view()),
    path('perfil/',PerfilView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    
]
