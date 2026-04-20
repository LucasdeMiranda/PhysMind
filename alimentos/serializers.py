from rest_framework import serializers


class AlimentoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    tipo = serializers.CharField()
    calorias = serializers.FloatField()
    proteinas = serializers.FloatField(allow_null=True)
    carboidratos = serializers.FloatField(allow_null=True)
    gordura = serializers.FloatField(allow_null=True)
    fibra = serializers.FloatField(allow_null=True)
    sodio = serializers.FloatField(allow_null=True)
    colesterol = serializers.FloatField(allow_null=True)
    gordurasaturada = serializers.FloatField(allow_null=True)