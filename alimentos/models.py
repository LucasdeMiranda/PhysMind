from django.db import models
from django.contrib.auth.models import User

class AlimentoBase(models.Model):#aliemntos que estão na tabela taco
    nome=models.CharField(max_length=30)
    calorias=models.IntegerField()#calorias proteinas carboidratos sodio fibras e etc tudo é baseado em 100 gramas do alimento
    proteinas=models.FloatField(null=True, blank=True)#gramas
    carboidratos=models.FloatField(null=True, blank=True)#gramas
    colesterol=models.FloatField(null=True,blank=True)#miligramas
    fibra=models.FloatField(null=True,blank=True)#gramas
    sodio=models.FloatField(null=True,blank=True)#
    
    def __str__(self):
        return f"{self.nome}"

class AlimentoCustomizado(models.Model):#alimentos que não estão na tabela que a pessoa comeu
    nome=models.CharField(max_length=100)
    calorias=models.IntegerField()
    proteinas=models.FloatField(null=True, blank=True)#gramas
    carboidratos=models.FloatField(null=True, blank=True)#gramas
    sodio=models.FloatField(null=True,blank=True)#miligramas
    gordura=models.FloatField(null=True,blank=True)
    gordurasaturada=models.FloatField(null=True,blank=True)
    fibra=models.FloatField(null=True,blank=True)#gramas
    usuario=models.ForeignKey(User,on_delete=models.CASCADE,related_name='alimentos')#se for deletado deleta tudo o que tem relação
    
    def __str__(self):
        return f"{self.nome} ({self.usuario.username})"
    
    
     