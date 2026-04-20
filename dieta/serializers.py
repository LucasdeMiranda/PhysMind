from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dieta, Refeicao, ConsumoAlimento

class ConsumoAlimentoSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    calorias = serializers.SerializerMethodField()
    proteinas = serializers.SerializerMethodField()
    carboidratos = serializers.SerializerMethodField()
    gordura = serializers.SerializerMethodField()
    
    class Meta:
        model = ConsumoAlimento
        fields = [
            'id',
            'quantidade',
            'nome',
            'calorias',
            'proteinas',
            'carboidratos',
            'gordura',
        ]
    def get_alimento(self, obj):
     return obj.alimentobase or obj.alimentocustomizado
    
    def get_calorias(self, obj):
        alimento = self.get_alimento(obj)
        if not alimento:
            return 0
        return (alimento.calorias * obj.quantidade) / 100
    
    def get_carboidratos(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return (alimento.carboidratos * obj.quantidade) / 100
    
    def get_proteinas(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return (alimento.proteinas * obj.quantidade) / 100
    
    def get_gordura(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        if alimento == obj.alimentocustomizado:
         return (alimento.gordura * obj.quantidade) / 100
    
        else:
          return None
    
    def get_nome(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return alimento.nome
    
 

# 🔹 REFEIÇÃO (agrupa vários consumos)
class RefeicaoSerializer(serializers.ModelSerializer):
    itens = ConsumoAlimentoSerializer(many=True, read_only=True)

    class Meta:
        model = Refeicao
        fields = [
            'id',
            'nome',
            'itens',
        ]


# 🔹 DIETA (nível principal)
class DietaSerializer(serializers.ModelSerializer):
    refeicoes = RefeicaoSerializer(many=True, read_only=True)

    class Meta:
        model = Dieta
        fields = [
            'id',
            'calorias',
            'proteinas',
            'carboidratos',
            'gordura',
            'refeicoes',
        ]

