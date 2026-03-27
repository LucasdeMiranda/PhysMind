from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dieta

class DietaSerializer(serializers.ModelSerializer):
    model=Dieta
    fields=[
        'calorias', 'proteinas', 'carboidratos', 'gordura'
    ]