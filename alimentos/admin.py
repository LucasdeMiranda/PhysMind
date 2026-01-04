from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import AlimentoBase
from .models import AlimentoCustomizado
from django.contrib.auth.models import User

@admin.register(AlimentoBase)
class AlimentoBaseAdmin(ImportExportModelAdmin):
    list_display=('nome','calorias','carboidratos','proteinas','colesterol','fibra','sodio')
    search_fields=('nome',)

@admin.register(AlimentoCustomizado)
class AlimentoCustomizadoAdmin(ImportExportModelAdmin):
    list_display=('nome','calorias','carboidratos','proteinas','sodio','fibra','usuario')
    list_filter=('usuario',)
    search_fields=('usuario__username','nome')