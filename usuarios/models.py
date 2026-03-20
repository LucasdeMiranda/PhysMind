from django.db import models
from django.contrib.auth.models import User # importa a classe prnta do user

class Perfil(models.Model):
     tipousuario=(('aluno','Aluno'),('profissional','Profissional'),('usuario_comum','Usuário Comum'))
     escolhaobjetivo=(('cutting','Cutting'),('bulking','Bulking'),('manutenção','Manutenção'))#nome que o usuario vai ver e o nome que vai ficar salvo no banco respectivamente
     escolhasexo=(('f','Feminino'),('m','Masculino'))#primeiro o que o banca grava o segundo o que o usuario vê
     nivelatividade=(('sedentario','Sedentário'),('moderado','Moderado'),('intenso','Intenso'),('leve','Leve'))
     usuario=models.OneToOneField(User,on_delete=models.CASCADE)# se o usuario forn deletado deleta todos os vinculos
     nome=models.CharField(max_length=30)
     tipo_usuario=models.CharField(max_length=20,choices=tipousuario)
     sexo=models.CharField(max_length=10,choices=escolhasexo,blank=True, null=True)
     altura=models.IntegerField(blank=True, null=True)#tudo em cm
     cintura=models.IntegerField(blank=True, null=True)
     pescoco=models.IntegerField(blank=True, null=True)
     objetivo=models.CharField(max_length=20,choices=escolhaobjetivo,blank=True, null=True)
     atividade=models.CharField(max_length=20,choices=nivelatividade,blank=True, null=True)
     idade=models.IntegerField(blank=True, null=True)
     
     def __str__(self):
      return f"{self.usuario.username} ({self.tipo_usuario})"
  
class ProfissionalAluno(models.Model):
    profissional=models.ForeignKey(User,on_delete=models.CASCADE,related_name='alunos')#pode ver todos os alunos que stão cadastrados com o profissional
    aluno=models.ForeignKey(User,on_delete=models.CASCADE,related_name='vinculo_profissional')#todos os profissionais que estão cadastrados a ele
    data=models.DateTimeField(auto_now_add=True)#data de inicio
    ativo=models.BooleanField(default=True)#se está ativo ou não o aluno
    class Meta:
        unique_together=('profissional','aluno')#não pode haver duplicações

    def __str__(self):
        return  f"{self.profissional.username}->{self.aluno.username}"# o jeito que vai aparecer no banco escrito

    
      
     
     
