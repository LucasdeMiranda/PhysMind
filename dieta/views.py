from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import DietaSerializer,RefeicaoSerializer,ConsumoAlimentoSerializer
from .models import Dieta,Refeicao,ConsumoAlimento
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError

# lista → get_queryset
# 1 objeto customizado → get_object
# criar → perform_create

class DietaView(RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=DietaSerializer
    
    def get_object(self):
     dieta=Dieta.objects.filter(
            usuario=self.request.user, ativo=True
        ).first()#pega adieta que ta ativa ou cria uma nova caso seja um novo usuário
     
     if not dieta:
         raise NotFound("nenhuma dieta ativa existente")
     return dieta

class RefeicoesView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefeicaoSerializer

    def get_queryset(self):# pega a primeira dieta que está ativa
        return Refeicao.objects.filter(
            usuario=self.request.user,
            dieta__ativo=True
        )

    def perform_create(self, serializer):#cria uma refeição
        dieta = Dieta.objects.filter(
            usuario=self.request.user,
            ativo=True
        ).first()

        if not dieta:
            raise ValidationError("Usuário não possui dieta ativa")

        serializer.save(
            usuario=self.request.user,
            dieta=dieta #salva usuario e dieta
        )
        
class RefeicaoDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefeicaoSerializer

    def get_queryset(self):
        return Refeicao.objects.filter(
            usuario=self.request.user,
            dieta__ativo=True
        )


class ConsumoAlimentoView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsumoAlimentoSerializer

    def get_queryset(self):
        return ConsumoAlimento.objects.filter(
            usuario=self.request.user,
            dieta__ativo=True#isso é fundamental para saber wual dieta usar se nao não saberia o que fazer
        )

    def perform_create(self, serializer):
        dieta = Dieta.objects.filter(
            usuario=self.request.user,
            ativo=True
        ).first()

        if not dieta:
            raise ValidationError("Usuário não possui dieta ativa")

        serializer.save(
            usuario=self.request.user,
            dieta=dieta
        )

class ConsumoAlimentoDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConsumoAlimentoSerializer

    def get_queryset(self):
        refeicao_id = self.request.query_params.get('refeicao')

        queryset = ConsumoAlimento.objects.filter(
            usuario=self.request.user,
            dieta__ativo=True
        )

        if refeicao_id:
            queryset = queryset.filter(refeicao_id=refeicao_id)

        return queryset#retorna os alimentos consumidos daquela refeição