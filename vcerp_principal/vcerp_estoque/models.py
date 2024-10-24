from django.db import models
from django.contrib.auth.models import User # type: ignore
from django.utils import timezone

# Create your models here.
class PessoaFisica(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14,  
 unique=True)
    email = models.EmailField(max_length=255)  

    telefone = models.CharField(max_length=15)
    rua = models.CharField(max_length=150)
    cep = models.CharField(max_length=8)
    ponto_referencia = models.CharField(max_length=150)
    penalizado = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')

    def __str__(self):
        return self.nome

class PessoaJuridica(models.Model):
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField(max_length=255)
    telefone = models.CharField(max_length=15)
    rua = models.CharField(max_length=150)
    cep = models.CharField(max_length=8)
    ponto_referencia = models.CharField(max_length=150)
    penalizado = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')

    def __str__(self):
        return self.razao_social


class Produto(models.Model):
    TIPOS = [
        ('eletronico', 'Eletrônico'),
        ('vestuario', 'Vestuário'),
        ('alimento', 'Alimento'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descricao = models.TextField()
    codigo_barra = models.CharField(max_length=50, unique=True)
    data_cadastro = models.DateField(auto_now_add=True)
    quantidade = models.PositiveIntegerField()
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.CharField(max_length=100, blank=True, null=True)
    unidade_medida = models.CharField(max_length=20)
    estoque_minimo = models.PositiveIntegerField(default=1)
    localizacao = models.CharField(max_length=100, blank=True, null=True)

    # Novo campo para imagem
    imagem_produto = models.ImageField(upload_to='produtos/', blank=True, null=True)

    def __str__(self):
        return self.nome

    def estoque_baixo(self):
        return self.quantidade < self.estoque_minimo

#Salvar o Contrato Gerado PJ
class Contrato_empresas(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14)
    campoendereco1 = models.CharField(max_length=100)
    campoendereco2 = models.CharField(max_length=100)
    campotel1 = models.CharField(max_length=20)
    campotel2 = models.CharField(max_length=20)
    campomaterial = models.CharField(max_length=100)
    periodo = models.IntegerField()
    dataentrega = models.DateField()
    datadevolve = models.DateField()
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user_contratoempresas",
        verbose_name='Usuário'
    )
    finalizado = models.BooleanField(default=False)

    def finalizar_contrato(self):
        self.finalizado = True
        self.save()

    def __str__(self):
        return self.nome

#Salvar o Contrato Gerado Pessoa Fisica
class Contrato_pessoa_fisica(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    campoendereco = models.CharField(max_length=100)
    campotel = models.CharField(max_length=20)
    campomaterial = models.CharField(max_length=100)
    periodo = models.IntegerField()
    dataentrega = models.DateField()
    datadevolve = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor do Pagamento')
    formapagamento = models.CharField(max_length=100, verbose_name='Forma de Pagamento')
    datapagamento = models.DateField()
    funcionario = models.CharField(max_length=100)
    ajudante = models.CharField(max_length=100)
        
    
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user_contratopessoafisica",
        verbose_name='Usuário'
    )

    def __str__(self):
        return self.nome
   


class Transacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    contrato = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=10, choices=(('entrada', 'Entrada'), ('saida', 'Saída')))
    data = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="user_transacao",
    )
    STATUS_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('baixa', 'Baixa realizada'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='entrada')
    data_baixa = models.DateTimeField(null=True, blank=True)
     


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
