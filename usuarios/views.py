from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response# retorna resposta autmaticamente renderizada em json ou html
from rest_framework import status# codigs 200,201,400 etc
from django.contrib.auth import authenticate #autenticar usuario existente
from usuarios.models import Perfil
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#APIView tranforma a classe em um edpoint http que entnde json porque
#o django esperaria um formulario html em vez disso e tambem permite entender os metodos post,get (http)

def gerar_token(user):
    refresh=RefreshToken.for_user(user)
    return{
        'access':str(refresh.access_token),
        'refresh':str(refresh),
    }
class CriaUsuario(APIView):#para responder requisições http rest
    def post(self,request):
        email=request.data.get('email')
        senha=request.data.get('senha')
        
        if not email or not senha:
              return Response(
                {'erro': 'Email e senha são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
              
        user= authenticate(username=email, password=senha)#username vira o próprio email
        
        if user:
            perfil= Perfil.objects.get(usuario=user)
            token=gerar_token(user)
            return Response({ 'status': 'existente', 'tipo_usuario': perfil.tipo_usuario,'mensagem':'Login realizado com suceso','access':token['acess'],'refresh':token['refresh'],},status=status.HTTP_200_OK)
        
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
        
class PerfilAutenticado(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        return Response({
            'email':request.user.email,
            'username':request.user.username,
        })

class ObtemPerfil(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        perfil=Perfil.objects.get(usuario=request.user)
        return Response({
            'nome': perfil.nome,
            'idade': perfil.idade,
            'altura': perfil.altura,
            'sexo': perfil.sexo,
            'tipo_usuario': perfil.tipo_usuario,
            'objetivo': perfil.objetivo,
            'cintura': perfil.cintura,
            'pescoco': perfil.pescoco,
        })
    
    def patch(self,request):
       perfil=ObtemPerfil.objects.get(usuario=request.user)
       CAMPOS_PERMITIDOS = [
        'nome', 'idade', 'altura', 'sexo',
        'tipo_usuario', 'objetivo',
        'cintura', 'pescoco'
    ]

       for campo, valor in request.data.items():
            if campo in CAMPOS_PERMITIDOS:
                setattr(perfil, campo, valor)

   
    


        
    
        
        
            
        
      
         
