from django.db import models
from django.contrib.auth.models import User
from alimentos.models import AlimentoBase, AlimentoCustomizado

class Dieta(models.Model):
     usuario=models.ForeignKey(User,on_delete=models.CASCADE,related_name='dietas')#se for deletado deleta tudo o que tem 
     calorias=models.IntegerField()#quantidade de calorias na dieta
     proteinas=models.FloatField()
     carboidratos=models.FloatField()
     gordura=models.FloatField()
     datacriacao=models.DateTimeField(auto_now_add=True)
     ativo=models.BooleanField(default=True)
     
     def __str__(self):
          return f"{self.usuario.username}"

class ConsumoAlimento(models.Model):
     usuario=models.ForeignKey(User,on_delete=models.CASCADE,related_name='consumos')#se for deletado deleta tudo o que tem 
     dieta=models.ForeignKey(Dieta,on_delete=models.CASCADE,related_name='consumos')
     alimentobase=models.ForeignKey(AlimentoBase,null=True,blank=True,on_delete=models.SET_NULL)
     alimentocustomizado=models.ForeignKey(AlimentoCustomizado,null=True,blank=True,on_delete=models.SET_NULL)
     quantidade=models.IntegerField()#em gramas
     data=models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
        if self.alimentobase:
          return f"{self.alimentobase.nome} ({self.quantidade}g)" 
        return f"{self.alimentocustomizado.nome} ({self.quantidade}g)"
     
 
    
    
     
