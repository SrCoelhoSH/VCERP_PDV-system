from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import (PessoaFisicaForm, PessoaJuridicaForm, 
                    ProdutoForm, SiginForms, 
                    SigupForms, UserUpdateForm,
                      ProfileUpdateForm, TransacaoForm,
                        Contrato_pessoa_fisicaForm, Contrato_empresasForm)
from .models import (PessoaFisica, PessoaJuridica,
                      Produto, Transacao, Profile,
                        Contrato_pessoa_fisica, Contrato_empresas)
from django.contrib import messages
from django.core.paginator import Paginator
import os
from docx import Document
from django.utils import timezone
from django.db.models import Sum
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io



def sigin(request):
    form = SiginForms()

    if request.method == 'POST':
        form = SiginForms(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome_sigin']
            senha = form.cleaned_data['password_sigin']

            usuario = authenticate(request, username=nome, password=senha)

            if usuario is not None:
                login(request, usuario)
                nome_completo = usuario.get_full_name()
                if nome_completo:
                    nomes = nome_completo.split()
                    primeiro_nome = nomes[0]
                    ultimo_nome = nomes[-1]
                    messages.success(request, f"Bem-vindo Sr(a) {primeiro_nome} {ultimo_nome}")
                else:
                    messages.success(request, f"Bem-vindo Sr(a){primeiro_nome} {ultimo_nome}")
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha inválidos, Solicite que o Administrador Verifique seu Cadastro')
                return redirect('sigin')

    return render(request, 'vcerp_estoque/sigin.html', {'form': form})

def sigup(request):
    form = SigupForms()

    if request.method == 'POST':
        form = SigupForms(request.POST)

        if form.is_valid():
            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                messages.error(request, 'As senhas precisam ser iguais')
                return redirect('signup')
            
            nome = form.cleaned_data['nome_cadastro']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['password1']

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Este nome de usuário já está em uso')
                return redirect('signup')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            messages.success(request, 'Conta criada com sucesso, Solicite o Administrador Verificar seu Cadastro.')
            return redirect('sigin')

    return render(request, 'vcerp_estoque/sigup.html', {'form': form})

def logout_view(request):
    logout(request)  # Função que realiza o logout
    messages.success(request, "Você saiu com sucesso.")  # Exibe uma mensagem de sucesso
    return redirect('sigin')  # Redireciona o usuário para a página de login após o logout
   
@login_required
def user_settings_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST.get('password')
        profile_image = request.FILES.get('profile_image')
        
        user = request.user
        
        # Atualizar nome de usuário e e-mail
        user.username = username
        user.email = email

        # Atualizar senha se fornecida
        if password:
            user.set_password(password)
            # Importante: manter o usuário autenticado após a troca de senha
            update_session_auth_hash(request, user)

        user.save()
        
        # Atualizar imagem de perfil, se fornecida
        if profile_image:
            profile = user.profile  # Supondo que o perfil já está criado
            profile.profile_image = profile_image
            profile.save()
        
        messages.success(request, 'Suas informações foram atualizadas com sucesso!')
        return redirect('user_settings')  # Redirecionar de volta para a página de configurações
    
    return render(request, 'vcerp_estoque/user_settings.html')



def index_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    return render(request, 'vcerp_estoque/index.html', {'usuario_logado': usuario_logado})

def dashboard_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    return render(request, 'vcerp_estoque/dashboard.html', {'usuario_logado': usuario_logado})


def estoque_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    produtos = Produto.objects.all()
    
    # Filtros de busca
    nome = request.GET.get('nome', '')
    tipo = request.GET.get('tipo', '')
    quantidade_min = request.GET.get('quantidade_min')
    quantidade_max = request.GET.get('quantidade_max')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if nome:
        produtos = produtos.filter(nome__icontains=nome)
    if tipo:
        produtos = produtos.filter(tipo=tipo)
    if quantidade_min:
        produtos = produtos.filter(quantidade__gte=quantidade_min)
    if quantidade_max:
        produtos = produtos.filter(quantidade__lte=quantidade_max)
    if data_inicio:
        produtos = produtos.filter(data_cadastro__gte=data_inicio)
    if data_fim:
        produtos = produtos.filter(data_cadastro__lte=data_fim)

    # Paginação
    itens_por_pagina = request.GET.get('itens_por_pagina', 10)
    paginator = Paginator(produtos, itens_por_pagina)
    page = request.GET.get('page')
    produtos = paginator.get_page(page)
    return render(request, 'vcerp_estoque/estoque.html', {'produtos': produtos, 'usuario_logado': usuario_logado})

   

def estoque_cadastro_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)  # Inclua request.FILES para lidar com uploads de arquivos
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('estoque_cadastro')
    else:
        form = ProdutoForm()
    
    return render(request, 'vcerp_estoque/estoque_cadastro.html', {'form': form, 'usuario_logado': usuario_logado})

def editar_produto_view(request, pk):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')

    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do Produto atualizados com sucesso!')
            return redirect('estoque')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'vcerp_estoque/estoque_editar_produto.html', {'form': form, 'usuario_logado': usuario_logado})

def deletar_produto_view(request, pk):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    produto = get_object_or_404(Produto, id=pk)
    
    if request.method == 'POST':
        try:
            produto.delete()
            messages.success(request, 'Produto excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir produto: {e}')
        return redirect('estoque')

    messages.error(request, 'Método não permitido para exclusão.')
    return redirect('vcerp_estoque/estoque')

def estoque_registra_transacao_view(request):
    usuario_logado = request.user
    
    if not request.user.is_authenticated:
        messages.error(request, 'É necessário estar logado para acessar esta página')
        return redirect('signin')
    
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        
        if form.is_valid():
            transacao = form.save(commit=False)
            produto = transacao.produto
            
            if transacao.tipo == 'entrada':
                produto.quantidade += transacao.quantidade
            else:
                if produto.quantidade < transacao.quantidade:
                    messages.error(request, 'Quantidade insuficiente em estoque')
                    return redirect('estoque_registra_transacao')
                else:
                    produto.quantidade -= transacao.quantidade
            
            produto.save()  # Salvar a alteração na quantidade do material
            transacao.save()  # Salvar a transação
            messages.error(request, 'Transação Realizada com Sucesso')
            return redirect('estoque')
    else:
        form = TransacaoForm()
    
    return render(request, 'vcerp_estoque/estoque_registra_transacao.html', {'form': form, 'usuario_logado': usuario_logado})

def estoque_detalhes_produto_view(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'vcerp_estoque/estoque_produto_detalhes.html', {'produto': produto})


def nota_recibo_view(request):
    

    return render(request, 'vcerp_estoque/nota_recibo.html')

def nota_fiscal_view(request):
    

    return render(request, 'vcerp_estoque/nota_fiscal.html')

def nota_gerar_contrato_cliente_view(request):
    

    return render(request, 'vcerp_estoque/nota_gerar_contrato_cliente.html')

def nota_gerar_contrato_empresas_view(request):
    

    return render(request, 'vcerp_estoque/nota_gerar_contrato_empresas.html')

def nota_orcamento_view(request):
    if request.method == 'POST':
        # Obtendo dados do formulário
        cliente = request.POST.get('cliente')
        data_orcamento = request.POST.get('data_orcamento')
        descricao = request.POST.getlist('descricao[]')
        quantidade = request.POST.getlist('quantidade[]')
        preco_unitario = request.POST.getlist('preco_unitario[]')
        total = request.POST.getlist('total[]')
        valor_total = request.POST.get('valor_total')

        # Convertendo quantidade e preço para valores numéricos
        quantidade = [int(q) for q in quantidade]
        preco_unitario = [float(p) for p in preco_unitario]
        total = [float(t) for t in total]

        # Criando o DataFrame
        df = pd.DataFrame({
            'Descrição': descricao,
            'Quantidade': quantidade,
            'Preço Unitário': preco_unitario,
            'Total': total
        })

        # Criação do PDF em memória
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        # Cabeçalho do PDF
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "Nota de Orçamento")
        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Cliente: {cliente}")
        p.drawString(100, 760, f"Data: {data_orcamento}")

        # Adicionando os itens do orçamento
        p.drawString(100, 740, "Itens Orçados:")
        x = 100
        y = 720

        for index, row in df.iterrows():
            # Adiciona nova página se necessário
            if y < 50:
                p.showPage()
                p.setFont("Helvetica", 12)
                y = 800
            p.drawString(x, y, f"Descrição: {row['Descrição']}, Quantidade: {row['Quantidade']}, Preço Unitário: R$ {row['Preço Unitário']}, Total: R$ {row['Total']}")
            y -= 20

        # Adiciona valor total
        p.drawString(100, y - 20, f"Valor Total: R$ {valor_total}")

        # Finaliza o PDF
        p.showPage()
        p.save()

        # Retorna o PDF como resposta
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='nota_orcamento.pdf')

    return render(request, 'vcerp_estoque/nota_orcamento.html')

def clientes_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    tipo_cliente = request.GET.get('tipo_cliente', '')
    busca = request.GET.get('busca', '')

    # Inicializa as listas de clientes
    clientes_pf = []
    clientes_pj = []

    # Filtra clientes com base no tipo e na busca
    if tipo_cliente == 'pf':
        if busca:
            clientes_pf = PessoaFisica.objects.filter(
                nome__icontains=busca) | PessoaFisica.objects.filter(cpf__icontains=busca)
        else:
            clientes_pf = PessoaFisica.objects.all()
    elif tipo_cliente == 'pj':
        if busca:
            clientes_pj = PessoaJuridica.objects.filter(
                razao_social__icontains=busca) | PessoaJuridica.objects.filter(cnpj__icontains=busca)
        else:
            clientes_pj = PessoaJuridica.objects.all()
    else:
        if busca:
            clientes_pf = PessoaFisica.objects.filter(
                nome__icontains=busca) | PessoaFisica.objects.filter(cpf__icontains=busca)
            clientes_pj = PessoaJuridica.objects.filter(
                razao_social__icontains=busca) | PessoaJuridica.objects.filter(cnpj__icontains=busca)
        else:
            clientes_pf = PessoaFisica.objects.all()
            clientes_pj = PessoaJuridica.objects.all()

    # Renderiza o template com a lista de clientes
    return render(request, 'vcerp_estoque/clientes.html', {
        'clientes_pf': clientes_pf,
        'clientes_pj': clientes_pj,
        'tipo_cliente': tipo_cliente,
        'busca': busca, 
        'usuario_logado': usuario_logado})
def clientes_cadastro_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin') 
    return render(request, 'vcerp_estoque/clientes_cadastro.html', {'usuario_logado': usuario_logado})

def clientes_cadastro_pf_view(request):
    if request.method == 'POST':
        form_pf = PessoaFisicaForm(request.POST)
        if form_pf.is_valid():
            form_pf.save()
            messages.success(request, 'Pessoa Física cadastrada com sucesso!')
            return redirect('clientes_cadastro_pf')
        else:
            print("Erros do formulário PF:", form_pf.errors)
            messages.error(request, 'Erro ao cadastrar Pessoa Física. Verifique os campos.')
    else:
        form_pf = PessoaFisicaForm()

    context = {
        'form_pf': form_pf,
    }

    return render(request, 'vcerp_estoque/clientes_cadastro_pf.html', context)
def clientes_cadastro_pj_view(request):
    usuario_logado = request.user  # Obtém o usuário logado
    
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    
    if request.method == 'POST':
        form_pj = PessoaJuridicaForm(request.POST)
        if form_pj.is_valid():
            form_pj.save()
            messages.success(request, 'Pessoa Jurídica cadastrada com sucesso!')
            return redirect('clientes_cadastro_pj')
        else:
            print("Erros do formulário PJ:", form_pj.errors)
            messages.error(request, 'Erro ao cadastrar Pessoa Jurídica. Verifique os campos.')
    else:
        form_pj = PessoaJuridicaForm()

    # Adiciona o usuário logado ao contexto
    context = {
        'form_pj': form_pj,
        'usuario_logado': usuario_logado,  # Passa o usuário logado para o template
    }

    return render(request, 'vcerp_estoque/clientes_cadastro_pj.html', context)

## Gera um novo contrato para pessoa juridica
def gerar_contrato_empresas(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    if request.method == 'POST':
        form = Contrato_empresasForm(request.POST)
        if form.is_valid():
            # Obtenha os dados do formulário
            cliente = form.cleaned_data['cliente']
            cnpj = form.cleaned_data['cnpj']
            campoendereco1 = form.cleaned_data['campoendereco1']
            campoendereco2 = form.cleaned_data['campoendereco2']
            campotel1 = form.cleaned_data['campotel1']
            campotel2 = form.cleaned_data['campotel2']
            campomaterial = form.cleaned_data['campomaterial']
            periodo = form.cleaned_data['periodo']
            dataentrega = form.cleaned_data['dataentrega']
            datadevolve = form.cleaned_data['datadevolve']
            
            # Salvar os dados do recibo no banco de dados
            recibo = Contrato_empresas.objects.create(nome=cliente, cnpj=cnpj, campoendereco1=campoendereco1,
                                            campoendereco2=campoendereco2, campotel1=campotel1, campotel2=campotel2,
                                             campomaterial=campomaterial, periodo=periodo, dataentrega=dataentrega, datadevolve=datadevolve, usuario=usuario_logado,
                                              )

            # Caminho para o arquivo modelo
            caminho_arquivo = os.path.join(os.path.dirname(__file__), 'docs/contrato_empresas.docx')

            # Carregar o arquivo modelo
            doc = Document(caminho_arquivo)

            # Substituir os marcadores de substituição dentro das tabelas
            substituir_texto_em_documento(doc, '{nome}', str(cliente))
            substituir_texto_em_documento(doc, '{campocnpj}', cnpj)
            substituir_texto_em_documento(doc, '{campoendereco1}', campoendereco1)
            substituir_texto_em_documento(doc, '{campoendereco2}', campoendereco2)
            substituir_texto_em_documento(doc, '{campotel1}', campotel1)
            substituir_texto_em_documento(doc, '{campotel2}', campotel2)
            substituir_texto_em_documento(doc, '{campomaterial}', campomaterial)
            substituir_texto_em_documento(doc, '{periododias}', str (periodo))
            substituir_texto_em_documento(doc, '{dataentrega}', str(dataentrega))
            substituir_texto_em_documento(doc, '{datadevolve}', str(datadevolve))
            

            # Nome do arquivo com base no nome e CPF fornecidos
            nome_arquivo = f'contrato_{cliente}_CNPJ_{cnpj}.docx'
            caminho_arquivo_modificado = os.path.join(os.path.dirname(__file__), 'contratos_temp_modificados', nome_arquivo)
            doc.save(caminho_arquivo_modificado)

            # Abre o arquivo .docx e retorna como resposta
            with open(caminho_arquivo_modificado, 'rb') as doc_file:
                response = HttpResponse(doc_file.read(), content_type='application/msword')
                response['Content-Disposition'] = f'attachment; filename={nome_arquivo}'
                return response

    else:
        form = Contrato_empresasForm()
    
    return render(request, 'vcerp_estoque/nota_gerar_contrato_empresas.html', {'form': form, 'usuario_logado': usuario_logado})

def editar_cliente_pf_view(request, pk):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    cliente = get_object_or_404(PessoaFisica, pk=pk)
    if request.method == 'POST':
        form = PessoaFisicaForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Pessoa Física atualizada com sucesso!')
            return redirect('clientes')  # Redirecionar para a lista de clientes
        else:
            messages.error(request, 'Erro ao atualizar os dados Pessoa Física. Verifique os campos abaixo.')
    else:
        form = PessoaFisicaForm(instance=cliente)
    
    context = {
        'form_pf': form,
        'cliente': cliente,
        'usuario_logado': usuario_logado,
    }
    
    return render(request, 'vcerp_estoque/editar_cliente_pf.html', context)

def editar_cliente_pj_view(request, pk):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    cliente = get_object_or_404(PessoaJuridica, pk=pk)
    if request.method == 'POST':
        form = PessoaJuridicaForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados Pessoa Jurídica atualizada com sucesso!')
            return redirect('clientes')  # Redirecionar para a lista de clientes
        else:
            messages.error(request, 'Erro ao atualizar os dados Pessoa Jurídica. Verifique os campos abaixo.')
    else:
        form = PessoaJuridicaForm(instance=cliente)
    
    context = {
        'form_pj': form,
        'cliente': cliente,
        'usuario_logado': usuario_logado,
    }
    
    return render(request, 'vcerp_estoque/editar_cliente_pj.html', context)

def alterar_status_cliente_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    cliente_id = request.GET.get('id')
    acao = request.GET.get('acao')

    if acao not in ['ativar', 'inativar']:
        messages.error(request, 'Ação inválida!')
        return redirect('clientes')

    cliente = get_object_or_404(PessoaFisica, id=cliente_id)
    if acao == 'ativar':
        cliente.status = 'ativo'
    else:
        cliente.status = 'inativo'

    cliente.save()
    messages.success(request, f'Cliente {acao} com sucesso!')
    return redirect('clientes', {'usuario_logado': usuario_logado})

def penalizar_cliente_view (request, cliente_id, tipo_cliente):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    if tipo_cliente == 'pf':
        cliente = get_object_or_404(PessoaFisica, id=cliente_id)
    elif tipo_cliente == 'pj':
        cliente = get_object_or_404(PessoaJuridica, id=cliente_id)
    else:
        return redirect('clientes')  # Redireciona para a lista de clientes se o tipo for inválido

    cliente.penalizado = True
    cliente.save()
    return redirect('clientes', {'usuario_logado': usuario_logado})  # Redireciona de volta para a lista de clientes
# Função para ativar ou inativar Pessoa Física
def ativar_inativar_pessoa_fisica(request, pk, action):
    pessoa = get_object_or_404(PessoaFisica, pk=pk)
    
    if action == 'ativar':
        pessoa.status = 'ativo'
        messages.success(request, f'Cliente {pessoa.nome} ativado com sucesso!')
    elif action == 'inativar':
        pessoa.status = 'inativo'
        messages.success(request, f'Cliente {pessoa.nome} inativado com sucesso!')
    
    pessoa.save()
    return redirect('clientes')  # redireciona para a página de listagem de pessoas

# Função para ativar ou inativar Pessoa Jurídica
def ativar_inativar_pessoa_juridica(request, pk, action):
    pessoa = get_object_or_404(PessoaJuridica, pk=pk)
    
    if action == 'ativar':
        pessoa.status = 'ativo'
        messages.success(request, f'Cliente {pessoa.razao_social} ativado com sucesso!')
    elif action == 'inativar':
        pessoa.status = 'inativo'
        messages.success(request, f'Cliente {pessoa.razao_social} inativado com sucesso!')
    
    pessoa.save()
    return redirect('clientes')  # redireciona para a página de listagem de pessoas jurídicas



def excluir_cliente_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')
    cliente_id = request.GET.get('id')
    if not cliente_id:
        return redirect('clientes')  # Redireciona se não houver ID

    cliente = get_object_or_404(PessoaFisica, id=cliente_id)  # Altere para PessoaJuridica se necessário
    cliente.delete()
    
    # Adicione uma mensagem de sucesso, se desejado
    messages.success(request, 'Cliente excluído com sucesso!')
    
    return redirect('clientes', {'usuario_logado': usuario_logado})

def rh_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')

    return render(request, 'vcerp_estoque/rh.html', {'usuario_logado': usuario_logado})

def rh_gerencias_funcionarios_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')

    return render(request, 'vcerp_estoque/rh_gerencias_funcionarios.html', {'usuario_logado': usuario_logado})

def rh_folha_pagamento_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')

    return render(request, 'vcerp_estoque/rh_folha_pagamento.html', {'usuario_logado': usuario_logado})

def rh_cadastrar_funcionarios_view(request):
    usuario_logado = request.user
    if not request.user.is_authenticated:
        messages.error(request, 'Precisa-se estar logado para acessar esta página')
        return redirect('sigin')

    return render(request, 'vcerp_estoque/rh_cadastrar_funcionarios.html', {'usuario_logado': usuario_logado})
