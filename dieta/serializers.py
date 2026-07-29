from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dieta, Refeicao, ConsumoAlimento
from rest_framework import status# codigs 200,201,400 etc


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
            'alimentobase',
            'alimentocustomizado',
            'refeicao',
        ]
        read_only_fields = ['nome', 'calorias', 'proteinas', 'carboidratos', 'gordura']
    
    def validate(self, attrs):
        alimentobase = attrs.get("alimentobase")
        alimentocustomizado = attrs.get("alimentocustomizado")

        if not alimentobase and not alimentocustomizado:
            raise serializers.ValidationError(
                "É necessário informar um alimento base ou um alimento customizado."
            )

        if alimentobase and alimentocustomizado:
            raise serializers.ValidationError(
                "Informe apenas um alimento: base ou customizado."
            )

        return attrs

    def get_alimento(self, obj):
     return obj.alimentobase or obj.alimentocustomizado

    def get_calorias(self, obj):
        alimento = self.get_alimento(obj)
        if not alimento:
            return 0
        return round((alimento.calorias * obj.quantidade) / 100,1)

    def get_carboidratos(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return round((alimento.carboidratos * obj.quantidade) / 100,1)

    def get_proteinas(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return round((alimento.proteinas * obj.quantidade) / 100,1)

    def get_gordura(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        if alimento == obj.alimentocustomizado:
         return round((alimento.gordura * obj.quantidade) / 100,1)

        else:
          return None

    def get_nome(self,obj):
        alimento=self.get_alimento(obj)
        if not alimento:
            return 0
        return alimento.nome



# REFEIÇÃO (agrupa vários consumos)
#faz o serializer acessar: refeicao.itens.all()
class RefeicaoSerializer(serializers.ModelSerializer):
    itens = ConsumoAlimentoSerializer(many=True, read_only=True)

    class Meta:
        model = Refeicao
        fields = [
            'id',
            'nome',
            'itens',
        ]


#DIETA (nível principal)
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
            'nome',
        ]

