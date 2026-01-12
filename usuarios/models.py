from django.db import models
from django.contrib.auth.models import User # importa a classe prnta do user

class Perfil(models.Model):
     tipousuario=(('aluno','Aluno'),('profissional','Profissional'))
     escolhaobjetivo=(('cutting','Cutting'),('bulking','Bulking'),('manutenção','Manutenção'))
     escolhasexo=(('f','Feminino'),('m','Masculino'))
     usuario=models.OneToOneField(User,on_delete=models.CASCADE)# se o usuario forn deletado deleta todos os vinculos
     nome=models.CharField(max_length=30)
     tipo_usuario=models.CharField(max_length=20,choices=tipousuario)
     sexo=models.CharField(max_length=10,choices=escolhasexo)
     altura=models.IntegerField()#tudo em cm
     cintura=models.IntegerField()
     pescoco=models.IntegerField()
     objetivo=models.CharField(max_length=20,choices=escolhaobjetivo)
     
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

    
      
     
     
