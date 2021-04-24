from django.urls import include, path

from projeto.estoque import views as v

app_name = 'estoque'


entrada_patterns = [
    path('', v.EstoqueEntradaList.as_view(), name='estoque_entrada_list'),
    path('add/', v.estoque_entrada_add, name='estoque_entrada_add'),
]

saida_patterns = [
    path('', v.EstoqueSaidaList.as_view(), name='estoque_saida_list'),
    path('add/', v.estoque_saida_add, name='estoque_saida_add'),
]

entrega_patterns = [
    path('', v.protocolo_de_entrega, name='protocolo_de_entrega_list'),
    path(
        '<int:pk>/',
        v.protocolo_de_entrega_detail,
        name='protocolo_de_entrega_detail'
    ),
    path(
        '<int:pk>/dar_baixa/',
        v.dar_baixa_no_estoque_com_protocolo_de_entrega,
        name='dar_baixa'
    ),
]

urlpatterns = [
    path('<int:pk>/', v.EstoqueDetail.as_view(), name='estoque_detail'),
    path('entrada/', include(entrada_patterns)),
    path('saida/', include(saida_patterns)),
    path('entrega/', include(entrega_patterns)),
]
