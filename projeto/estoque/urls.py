from django.urls import path
from projeto.estoque import views as v


app_name = 'estoque'


urlpatterns = [
    path('', v.estoque_entrada_list, name='estoque_entrada_list'),
]
