from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from vcerp_estoque.models import Produto
from .models import Caixa, CaixaLog

# View da página inicial do caixa
@csrf_exempt
@login_required
def vcerp_caixa_index_view(request):
    context = {}

    # Obtenha o caixa associado ao usuário, se existir
    caixa_atual = Caixa.objects.filter(usuario=request.user, status='ocupado').first()

    if caixa_atual:
        context['caixa_id'] = caixa_atual.id
        context['usuario_nome'] = request.user.get_full_name() or request.user.username
    else:
        context['caixa_id'] = None
        context['usuario_nome'] = request.user.get_full_name() or request.user.username

    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'iniciar_venda':
            context['message'] = "Venda iniciada com sucesso!"

        elif action == 'cancelar_item':
            context['message'] = "Item cancelado!"

        elif action == 'finalizar_venda':
            context['message'] = "Venda finalizada com sucesso!"

        elif action == 'abrir_configuracoes':
            context['message'] = "Abrindo menu de configurações..."

        elif action == 'consulta_preco':
            codigo_barra = data.get('codigo_barra')
            produto = Produto.objects.filter(codigo_barra=codigo_barra).first()

            if produto:
                produto_data = {
                    'id': produto.id,
                    'nome': produto.nome,
                    'descricao': produto.descricao,
                    'preco_venda': produto.preco_venda,
                    'unidade_medida': produto.unidade_medida,
                    'imagem_produto': produto.imagem_produto.url if produto.imagem_produto else 'default-image.png'
                }
                context['produto'] = produto_data
                context['message'] = "Produto encontrado!"
            else:
                context['message'] = "Produto não encontrado"

        elif action == 'adicionar_ao_carrinho':
            produto_id = data.get('produto_id')
            produto = get_object_or_404(Produto, id=produto_id)
            carrinho = request.session.get('carrinho', [])
            carrinho.append(produto_id)
            request.session['carrinho'] = carrinho
            context['message'] = "Produto adicionado ao carrinho!"

        return JsonResponse(context)

    return render(request, 'vcerp_caixa/index_caixa.html', context)

# View para buscar um produto pelo código de barras (modificada)
def buscar_produto(request):
    codigo_barra = request.GET.get('codigo_barra')
    try:
        produto = Produto.objects.get(codigo_barra=codigo_barra)
        data = {
            'nome': produto.nome,
            'preco_unitario': str(produto.preco_venda),  # Converter para string aqui
            # ... outros dados do produto que você precisa ...
        }
        return JsonResponse(data)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Erro interno ao buscar o produto.'}, status=500)

@csrf_exempt
@login_required
def cancelar_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            itens_para_cancelar = data.get('itens')

            # Lógica para cancelar os itens (exemplo):
            for item in itens_para_cancelar:
                seq = item.get('seq')
                nome = item.get('nome')
                # ... lógica para cancelar o item com base nos dados ...
                print(f"Item cancelado: Seq {seq}, Nome: {nome}")

            return JsonResponse({'message': 'Itens cancelados com sucesso!'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)


# View para o login do usuário
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('selecionar_caixa')  # Redireciona para a seleção de caixa após o login
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'vcerp_caixa/sigin_caixa.html')


# View para selecionar um caixa disponível e abrir o caixa
@login_required
def selecionar_caixa_view(request):
    caixas_disponiveis = Caixa.objects.filter(status='disponivel')

    if request.method == 'POST':
        caixa_id = request.POST.get('caixa_id')
        caixa_selecionado = get_object_or_404(Caixa, id=caixa_id)
        if caixa_selecionado.status == 'disponivel':
            caixa_selecionado.usuario = request.user
            caixa_selecionado.abrir()  # Chama o método para abrir o caixa
            
            # Registra a ação no log
            CaixaLog.objects.create(caixa=caixa_selecionado, usuario=request.user, acao='abertura')

            return redirect('vcerp_caixa_index')
        else:
            return render(request, 'selecionar_caixa.html', {'error': 'Caixa já está ocupado', 'caixas': caixas_disponiveis})
    
    return render(request, 'vcerp_caixa/selecionar_caixa.html', {'caixas': caixas_disponiveis})


# View para fechar o caixa atualmente aberto pelo usuário
@login_required
def fechar_caixa_view(request):
    if request.method == 'POST':
        caixa_aberto = Caixa.objects.filter(usuario=request.user, status='ocupado').first()

        if caixa_aberto:
            caixa_aberto.fechar()  # Chama o método para fechar o caixa
            
            # Registra a ação no log
            CaixaLog.objects.create(caixa=caixa_aberto, usuario=request.user, acao='fechamento')

            return JsonResponse({'success': True, 'message': 'Caixa fechado com sucesso!'})
        else:
            return JsonResponse({'success': False, 'message': 'Nenhum caixa aberto encontrado para este usuário.'})

    return JsonResponse({'success': False, 'message': 'Método inválido.'})


# View para fechar um caixa específico
@login_required
def vcerp_caixa_fechar_view(request, caixa_id):
    if request.method == 'POST':
        caixa_aberto = get_object_or_404(Caixa, id=caixa_id, usuario=request.user, status='ocupado')

        if caixa_aberto:
            caixa_aberto.status = 'disponivel'  # Altera o status para "disponível"
            caixa_aberto.usuario = None  # Remove a vinculação do usuário
            caixa_aberto.data_fechamento = timezone.now()  # Registra a data e hora de fechamento
            caixa_aberto.save()

            return JsonResponse({'success': True, 'message': 'Caixa fechado com sucesso!'})
        else:
            return JsonResponse({'success': False, 'message': 'Nenhum caixa aberto encontrado para este usuário.'})

    return JsonResponse({'success': False, 'message': 'Método inválido.'})
