from django.urls import path
from projeto.estoque import views as v


app_name = 'estoque'


urlpatterns = [
    path('', v.EstoqueEntradaList.as_view(), name='estoque_entrada_list'),
    path('<int:pk>/', v.EstoqueDetail.as_view(), name='estoque_detail'),
    path('add/', v.estoque_entrada_add, name='estoque_entrada_add'),
    path('saida/', v.EstoqueSaidaList.as_view(), name='estoque_saida_list'),
    path('saida/add/', v.estoque_saida_add, name='estoque_saida_add'),
]
