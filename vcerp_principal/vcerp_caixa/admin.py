from django.contrib import admin
from .models import Caixa, CaixaLog

@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'status', 'usuario')
    list_filter = ('status',)
    search_fields = ('numero', 'usuario__username')


@admin.register(CaixaLog)
class CaixaLogAdmin(admin.ModelAdmin):
    list_display = ('caixa', 'usuario', 'acao', 'data_hora')
    list_filter = ('acao', 'data_hora')
