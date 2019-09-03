from django.urls import path
from projeto.produto import views as v


app_name = 'produto'


urlpatterns = [
    path('', v.ProdutoList.as_view(), name='produto_list'),
    path('<int:pk>/', v.produto_detail, name='produto_detail'),
    path('add/', v.ProdutoCreate.as_view(), name='produto_add'),
    path('<int:pk>/edit/', v.ProdutoUpdate.as_view(), name='produto_edit'),
    path('<int:pk>/json/', v.produto_json, name='produto_json'),
    path('import/csv/', v.import_csv, name='import_csv'),
]
