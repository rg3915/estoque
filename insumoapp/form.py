from django.forms import ModelForm
from .models import Produto


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo', 'descricao', 'tipo']


class ProducaoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo', 'descricao', 'tipo']
