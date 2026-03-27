from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import DietaSerializer
from .models import Dieta
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

class DietaView(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DietaSerializer
    
    def get_object(self):
     dieta=Dieta.objects.filter(
            usuario=self.request.user, ativo=True
        ).first#pega adieta que ta ativa ou cria uma nova caso seja um novo usuário
     
     if not dieta:
         raise NotFound("")
     return dieta
 
           
