from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response# retorna resposta autmaticamente renderizada em json ou html
from rest_framework import status# codigs 200,201,400 etc
from django.contrib.auth import authenticate #autenticar usuario existente

#APIView tranforma a classe em um edpoint http que entnde json porque
#o django esperaria um formulario html em vez disso e tambem permite entender os metodos post,get (http)

class CriaUsuario(APIView):#para responder requisições http rest
    def post(self,request):
        email=request.data.get('email')
        senha=request.data.get('senha')
        
        if not email or not senha:
              return Response(
                {'erro': 'Email e senha são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
              
        user= authenticate(username=email, password=senha)
        
        if user:
            return Response({'mensagem':'Login realizado com suceso'},status=status.HTTP_200_OK)
        
        if User.objects.filter(username=email).exists():
            return Response({'mensagem':'Senha ou Email incorreta'},status=status.HTTP_401_UNAUTHORIZED)
    
    
        user = User.objects.create_user(# cria o usuario caso ele não exista
            username=email,
            email=email,
            password=senha
        )

        return Response(
            {'mensagem': 'Usuário criado com sucesso'},
            status=status.HTTP_201_CREATED
        )
            
        
      
         
