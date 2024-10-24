from django import forms
from .models import ( PessoaJuridica, PessoaFisica,
                      Produto, Profile, 
                      Transacao, Contrato_empresas, 
                      Contrato_pessoa_fisica )
from django.contrib.auth.models import User


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = ['nome', 'cpf', 'email', 'telefone', 'rua', 'cep', 'ponto_referencia']
        widgets = {
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
        }

class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = ['razao_social', 'cnpj', 'email', 'telefone', 'rua', 'cep', 'ponto_referencia']
        widgets = {
            'cnpj': forms.TextInput(attrs={'placeholder': '00.000.000/0000-00'}),
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
        }


class CustomClienteSearchForm(forms.Form):
    search_query = forms.CharField(label='Pesquisar Cliente', max_length=100, required=False)

    def get_client_data(self):
        search_query = self.cleaned_data.get('search_query')
        if search_query:
            try:
                cliente = PessoaJuridica.objects.get(cliente_username=search_query)
                return {
                    'pessoajuridica_razao': pessoajuridica.pessoajuridica_razao,
                    'pessoajuridica_cnpj': pessoajuridica.pessoajuridica_cnpj,
                    'pessoajuridica_telefone': pessoajuridica.pessoajuridica_telefone,
                    'pessoajuridica_endereco': pessoajuridica.pessoajuridica_endereco,
                }
            except PessoaJuridica.DoesNotExist:
                return None
        return None


class Contrato_empresasForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=PessoaJuridica.objects.all(), label='Cliente', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Contrato_empresas
        fields = ['nome', 'cnpj', 'campoendereco1', 'campoendereco2', 'campotel1',
                   'campotel2', 'campomaterial', 'periodo', 'dataentrega', 'datadevolve']
        labels = {
            'cnpj': 'CNPJ: Ex: 00.000.000/0000-00',
            'campoendereco1': 'Endereço da empresa',
            'campoendereco2': 'Endereço da Obra',
            'campotel1': 'Telefone da empresa',
            'campotel2': 'Celular da empresa',
            'datainicial2': 'Data Inicial 2',
            'campomaterial': 'Material alocados',
            'periodo': 'Período "Digitar Somente Numeros"',
            'dataentrega': 'data de entrega',
            'datadevolve': 'data de devolução',
          
        }
        widgets = {
            'dataentrega': forms.DateInput(attrs={'type': 'date'}),
            'datadevolve': forms.DateInput(attrs={'type': 'date'}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = PessoaJuridica.objects.all()    

class Contrato_pessoa_fisicaForm(forms.ModelForm):
    FORMAS_PAGAMENTO_CHOICES = [
        ('Cartão de credito 1x', 'Cartão de Crédito 1x'),
        ('Cartão de credito 2x', 'Cartão de Crédito 2x'),
        ('Cartão de credito x3', 'Cartão de Crédito 3x'),
        ('Cartão de credito x4', 'Cartão de Crédito 4x'),
        ('Cartão de credito x5', 'Cartão de Crédito 5x'),
        ('Cartão de credito x6', 'Cartão de Crédito 6x'),
        ('Cartão de credito x7', 'Cartão de Crédito 7x'),
        ('Cartão de credito x8', 'Cartão de Crédito 8x'),
        ('Cartão de credito x9', 'Cartão de Crédito 9x'),
        ('Cartão de credito x10', 'Cartão de Crédito 10x'),
        ('Cartão de credito x11', 'Cartão de Crédito 11x'),
        ('Cartão de credito x12', 'Cartão de Crédito 12x'),
        ('Cartão de debito', 'Cartão de Débito'),
        ('Pix', 'Pix'),
        ('Especie', 'Dinheiro/Espécie'),
        # Adicione outras opções de pagamento conforme necessário
    ]
    formapagamento = forms.ChoiceField(choices=FORMAS_PAGAMENTO_CHOICES, label='Forma de Pagamento', widget=forms.Select(attrs={'class': 'form-control'}))
    
    cliente = forms.ModelChoiceField(queryset=PessoaFisica.objects.all(), label='Cliente', widget=forms.Select(attrs={'class': 'form-control'}))
   # funcionario = forms.ModelChoiceField(queryset=Funcionario.objects.all(), label='Funcionaro', widget=forms.Select(attrs={'class': 'form-control'}))
  #  ajudante = forms.ModelChoiceField(queryset=Funcionario.objects.all(), label='Ajudante', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Contrato_pessoa_fisica
        fields = ['nome', 'cpf', 'campoendereco', 'campotel',
                    'campomaterial', 'periodo', 'dataentrega', 'datadevolve','valor', 'formapagamento', 'datapagamento','funcionario', 'ajudante']
        labels = {
            'cpf': 'CPF: Ex: 000.000.000-00',
            'campoendereco': 'Endereço da entrega', 
            'campotel': 'Telefone ou Celular',
            'dataentrega': 'Data de entrega 2',
            'datadevolve': 'Data de coleta',
            'periodo': 'Período "Digitar Somente Numeros"',
            'valor': 'Valor do Pagamento',
            'formapagamento': 'Forma de Pagamento',
            'datapagamento': 'Data de Pagamento',
            'funcionario': 'Funcionário',
            'ajudante': 'Ajudante',
        }
        widgets = {
            'dataentrega': forms.DateInput(attrs={'type': 'date'}),
            'datadevolve': forms.DateInput(attrs={'type': 'date'}),
            'datapagamento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = PessoaFisica.objects.all()


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo', 'descricao', 'codigo_barra', 'quantidade', 'preco_compra', 'preco_venda', 'fornecedor', 'unidade_medida', 'estoque_minimo', 'localizacao', 'imagem_produto']





class SiginForms(forms.Form):
    nome_sigin = forms.CharField(
        label='Nome de Login',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: Pablo"
        })
    )
    
    password_sigin = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: Digite sua senha"
        })
    )
class SigupForms(forms.Form):
    nome_cadastro = forms.CharField(
        label='Digite seu nome de usuário',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: nome.sobrenome"})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex.: exemplo@xyx.com"})
    )
    password1 = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ex: Digite sua senha"})
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Ex: Digite novamente sua senha"})
    )


    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')

        if nome:
            nome = nome.strip()
            if " " in nome:
                raise forms.ValidationError("O nome de usuário não pode conter espaços.")
            else:
                return nome


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['produto', 'quantidade','contrato','tipo']

