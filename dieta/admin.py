from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import User
from alimentos.models import AlimentoBase, AlimentoCustomizado
from .models import Dieta
from .models import ConsumoAlimento


@admin.register(Dieta)
class DietaAdmin(ImportExportModelAdmin):
    list_display=('usuario','calorias','proteinas','carboidratos','gordura','datacriacao','ativo')
    list_filter=('datacriacao',)
    search_fields=('usuario__username',)

@admin.register(ConsumoAlimento)
class ConsumoAlimentoAdmin(ImportExportModelAdmin):
    list_display=('usuario','dieta','alimentobase','alimentocustomizado','quantidade','data')
    list_filter=('data','usuario__username',)
    search_fields=('usuario__username',)

# Register your models here.
