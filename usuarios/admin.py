from django.contrib import admin
from .models import Perfil
from .models import ProfissinalAluno
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User

@admin.register(Perfil)
class PerfilAdmin(ImportExportModelAdmin):
    list_display=('tipo_usuario','usuario','sexo','altura','cintura','pescoco','objetivo')
    list_filter=('tipo_usuario','sexo',)
    search_fields=('usuario__username','usuario__email',)

@admin.register(ProfissinalAluno)
class ProfissionalAlunoAdmin(ImportExportModelAdmin):
    list_display=('profissional','aluno','data','ativo')
    list_filter=('ativo',)
    search_fields=('profissional__username','aluno__username',)
    
    
