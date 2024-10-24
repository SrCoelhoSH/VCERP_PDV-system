from django.contrib import admin
from .models import Caixa

@admin.register(Caixa)
class CaixaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'status', 'usuario')
    list_filter = ('status',)
    search_fields = ('numero', 'usuario__username')