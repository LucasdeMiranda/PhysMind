from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CriaUsuario(APIView):
    def post(self,request):
        email=request.data.get('email')
        senha=request.data.get('senha')
        
        if not email or not senha:
              return Response(
                {'erro': 'Email e senha são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=email).exists():
            return Response(
                {'erro': 'Usuário já existe'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha
        )

        return Response(
            {'mensagem': 'Usuário criado com sucesso'},
            status=status.HTTP_201_CREATED
        )
            
        
      
         
