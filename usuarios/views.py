from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response# retorna resposta autmaticamente renderizada em json ou html do http
from rest_framework import status# codigs 200,201,400 etc
from django.contrib.auth import authenticate #autenticar usuario existente
from usuarios.models import Perfil
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import CriaUsuarioSerializer
from .serializers import  PerfilSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView

#APIView tranforma a classe em um edpoint http que entnde json porque
#o django esperaria um formulario html em vez disso e tambem permite entender os metodos post,get (http)

def gerar_token(user):
    refresh=RefreshToken.for_user(user)
    return{
        'access':str(refresh.access_token),
        'refresh':str(refresh),
    }
class CriaUsuario(APIView):#para responder requisições http rest
    @swagger_auto_schema(request_body=CriaUsuarioSerializer)
    def post(self,request):
        print("Dados brutos:", request.data)
        serializer=CriaUsuarioSerializer(data=request.data)#usado para fazer o json virr algo valido no python e poder ser validádo
        if not serializer.is_valid():
              print("ERRO DE VALIDAÇÃO:", serializer.errors)
              return Response(
                serializer.errors, status=400
            )
        print("Dados validados:", serializer.validated_data)
        print("Usuário não existe, criando novo usuário...")
        email = serializer.validated_data['email']
        senha = serializer.validated_data['senha']
              
        user= authenticate(username=email, password=senha)#username vira o próprio email
        print("Usuário autenticado:", user)
        
        if user:
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            token=gerar_token(user)#para gerar o token de acesso no caso do usuario ja existe 
            return Response({ 'status': 'existente', 'tipo_usuario': perfil.tipo_usuario,'mensagem':'Login realizado com suceso','access':token['access'],'refresh':token['refresh'],},status=status.HTTP_200_OK)
        
        if User.objects.filter(username=email).exists():
            return Response({'mensagem':'Senha ou Email incorreta'},status=status.HTTP_401_UNAUTHORIZED)    
        user = User.objects.create_user(# cria o usuario caso ele não exista
            username=email,
            email=email,
            password=senha
        )

        token=gerar_token(user)
        return Response(
            { 'status': 'novo','mensagem': 'Usuário criado com sucesso','access':token['access'],'refresh':token['refresh'],},
            status=status.HTTP_201_CREATED
        )
        
class PerfilView(RetrieveUpdateAPIView):#essa é uma classe pronta que vem de .generics que implementa os metodos patch/get/put
    permission_classes=[IsAuthenticated] #permission e uma configuração do endpoint regras de acesso 
    serializer_class=PerfilSerializer# serializer usado para converter o objeto Perfil em dados JSON na resposta da API
    def get_object(self):
        perfil,created=Perfil.objects.get_or_create(
            usuario=self.request.user
        )
        return perfil#precisa do serializer porque precisa retornar um json entao ele faz isso internamente
    #perfil = self.get_object()
#serializer = PerfilSerializer(perfil)
#return Response(serializer.data)
#não da pra trocar pbjetos entre si entao tem que ser json 
    
                

   
    


        
    
        
        
            
        
      
         
