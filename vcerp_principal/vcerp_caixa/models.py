from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Caixa(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupado', 'Ocupado'),
        ('fechado', 'Fechado'),  # Adicionando a opção "fechado"
    ]

    numero = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_abertura = models.DateTimeField(null=True, blank=True)  # Data e hora de abertura
    data_fechamento = models.DateTimeField(null=True, blank=True)  # Data e hora de fechamento

    def abrir(self):
        """Método para registrar a abertura do caixa"""
        self.status = 'ocupado'
        self.data_abertura = timezone.now()
        self.save()

    def fechar(self):
        """Método para registrar o fechamento do caixa"""
        self.status = 'fechado'
        self.data_fechamento = timezone.now()
        self.usuario = None
        self.save()

    def __str__(self):
        return f'Caixa {self.numero} - {self.status}'
    

class CaixaLog(models.Model):
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=10, choices=[('abertura', 'Abertura'), ('fechamento', 'Fechamento')])
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.acao.capitalize()} do Caixa {self.caixa.numero} por {self.usuario.username} em {self.data_hora}'