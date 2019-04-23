from django.urls import path
from projeto.estoque import views as v


app_name = 'estoque'


urlpatterns = [
    path('', v.estoque_entrada_list, name='estoque_entrada_list'),
    path('<int:pk>/', v.estoque_entrada_detail, name='estoque_entrada_detail'),
    path('add/', v.estoque_entrada_add, name='estoque_entrada_add'),
]
