from django.urls import path
from vcerp_estoque.views import sigin, sigup,logout_view,user_settings_view , index_view, estoque_view, estoque_cadastro_view, estoque_registra_transacao_view, estoque_detalhes_produto_view , nota_recibo_view, nota_fiscal_view, nota_gerar_contrato_cliente_view, nota_gerar_contrato_empresas_view, nota_orcamento_view, clientes_cadastro_view, clientes_view, rh_view, rh_gerencias_funcionarios_view, rh_cadastrar_funcionarios_view, rh_folha_pagamento_view, clientes_cadastro_pf_view, clientes_cadastro_pj_view, editar_cliente_pf_view, editar_cliente_pj_view, alterar_status_cliente_view, penalizar_cliente_view, excluir_cliente_view, editar_produto_view, deletar_produto_view, ativar_inativar_pessoa_fisica, ativar_inativar_pessoa_juridica, dashboard_view, gerar_contrato_empresas
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', sigin, name='sigin'),
    path('register/', sigup, name='sigup'),
    path('logout/', logout_view, name='logout'),
    path('index/', index_view, name='index'),
    path('index/user_settings', user_settings_view, name='user_settings'),
    path('index/dashboard', dashboard_view, name='dashboard'),
   
   
    path('index/estoque', estoque_view, name='estoque'),
    path('index/estoque_cadastro', estoque_cadastro_view, name='estoque_cadastro'),
    path('index/estoque_registra_transacao', estoque_registra_transacao_view, name='estoque_registra_transacao'),
    path('produto/detalhes/<int:pk>/', estoque_detalhes_produto_view, name='estoque_detalhes_produto'),


    path('produto/editar/<int:pk>/', editar_produto_view, name='editar_produto'),
    path('produto/excluir/<int:pk>/', deletar_produto_view, name='deletar_produto'),

   
   
    path('index/nota_recibo', nota_recibo_view, name='nota_recibo'),
    path('index/nota_fiscal', nota_fiscal_view, name='nota_fiscal'),
    path('index/nota_gerar_contrato_cliente', nota_gerar_contrato_cliente_view, name='nota_gerar_contrato_cliente'),
    path('index/nota_gerar_contrato_empresas', gerar_contrato_empresas, name='nota_gerar_contrato_empresas'),
    path('index/nota_orcamento', nota_orcamento_view, name='nota_orcamento'),
   


    path('index/clientes', clientes_view, name='clientes'),
    path('index/clientes_cadastro', clientes_cadastro_view, name='clientes_cadastro'),
    path('index/clientes_cadastro_pf', clientes_cadastro_pf_view, name='clientes_cadastro_pf'),
    path('index/clientes_cadastro_pj', clientes_cadastro_pj_view, name='clientes_cadastro_pj'),
    path('index/clientes/editar/pf/<int:pk>/', editar_cliente_pf_view, name='editar_cliente_pf'),
    path('index/clientes/editar/pj/<int:pk>/', editar_cliente_pj_view, name='editar_cliente_pj'),
    path('index/alterar_status_cliente/', alterar_status_cliente_view, name='alterar_status_cliente'),
    path('index/penalizar_cliente/<int:cliente_id>/<str:tipo_cliente>/', penalizar_cliente_view, name='penalizar_cliente'),
    path('index/excluir_cliente/', excluir_cliente_view, name='excluir_cliente'),
    path('pessoa_fisica/<int:pk>/<str:action>/', ativar_inativar_pessoa_fisica, name='alterar_status_cliente_pf'),
    path('pessoa_juridica/<int:pk>/<str:action>/', ativar_inativar_pessoa_juridica, name='alterar_status_cliente_pj'),
    
    
    path('index/rh', rh_view, name='rh'),
    path('index/rh_gerencias_funcionarios', rh_gerencias_funcionarios_view, name='rh_gerencias_funcionarios'),
    path('index/rh_cadastrar_funcionarios', rh_cadastrar_funcionarios_view, name='rh_cadastrar_funcionarios'),
    path('index/rh_folha_pagamento', rh_folha_pagamento_view, name='rh_folha_pagamento'),
] 

# Para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)