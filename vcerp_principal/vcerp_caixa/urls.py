from django.urls import path
from vcerp_caixa.views import (
    vcerp_caixa_index_view,
    login_view,
    vcerp_caixa_fechar_view,
    selecionar_caixa_view,
    fechar_caixa_view,
    buscar_produto,  # Importe a nova view
    cancelar_item     # Importe a view cancelar_item
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', login_view, name='login'),
    path('selecionar-caixa/', selecionar_caixa_view, name='selecionar_caixa'),
    path('fechar-caixa/', fechar_caixa_view, name='fechar_caixa'),
    path('caixa/', vcerp_caixa_index_view, name='vcerp_caixa_index'),
    path('caixa/fechar/<int:caixa_id>/', vcerp_caixa_fechar_view, name='vcerp_fechar_caixa'),
    path('buscar_produto/', buscar_produto, name='buscar_produto'),
    path('cancelar_item/', cancelar_item, name='cancelar_item')  # Nova URL para cancelar_item
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)