from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil

class CriaUsuarioSerializer(serializers.Serializer):
    email=serializers.EmailField()
    senha= serializers.CharField(write_only=True)
    

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model=Perfil
        fields=[
             'nome',
            'tipo_usuario',
            'sexo',
            'altura',
            'cintura',
            'pescoco',
            'objetivo',
            'atividade',
            'idade'
        ]
        read_only_fields = []