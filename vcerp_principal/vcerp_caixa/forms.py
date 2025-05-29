from django import forms
from .models import Caixa

class CaixaForm(forms.ModelForm):
    """Formulário básico para criação e edição de caixas."""

    class Meta:
        model = Caixa
        fields = [
            'numero',
            'status',
            'usuario',
            'data_abertura',
            'data_fechamento',
        ]
        widgets = {
            'data_abertura': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fechamento': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
