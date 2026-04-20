from django.shortcuts import render
from .serializers import AlimentoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response# retorna resposta autmaticamente renderizada em json ou html do http
from rest_framework import status# codigs 200,201,400 etc
from django.contrib.auth import authenticate #autenticar usuario existente
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import AlimentoBase,AlimentoCustomizado
from django.contrib.auth.models import User

# como isso não pe um crud  tradicional nao consigo usar views genricas ja implementadas
class AlimentoView(APIView):
    permission_classes= [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Lista de Alimentos base e os cutomizados do usuário",
        responses={200:AlimentoSerializer(many=True)}#esse many true é porque é uma lista de objetos e nao só um
    )
    def get(self, request):
        query= request.query_params.get('search','')#url/:search=arroz por isso isso aqui
        base= AlimentoBase.objects.filter(nome__icontains=query)
        customizado=AlimentoCustomizado.objects.filter( usuario=request.user,nome__icontains=query)# esse usuario=request.user é
        #o que garante que somente o usuário veja seus alimentos personalizados
        resultado=[]
        
        for alimento in base:
            resultado.append({
            "id":alimento.id,
            "nome": alimento.nome,
            "tipo": "base",
            "calorias": alimento.calorias,
            "proteinas": alimento.proteinas,
            "carboidratos": alimento.carboidratos,
            "gordura": None,
            "fibra": alimento.fibra,
            "sodio": alimento.sodio,
            "colesterol": alimento.colesterol,
            "gordurasaturada": None,               
            }
            )
        
        for alimento in customizado:
            resultado.append({
                "id": alimento.id,
                "nome": alimento.nome,
                "tipo": "custom",
                "calorias": alimento.calorias,
                "proteinas": alimento.proteinas,
                "carboidratos": alimento.carboidratos,
                "gordura": alimento.gordura,
                "fibra": alimento.fibra,
                "sodio": alimento.sodio,
                "colesterol": None,
                "gordurasaturada": alimento.gordurasaturada,
            })
        serializer=AlimentoSerializer(resultado,many=True)
        return Response(serializer.data)
            