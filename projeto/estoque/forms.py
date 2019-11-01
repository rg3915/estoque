from django import forms
from .models import Estoque, EstoqueItens
from projeto.produto.models import Produto


class EstoqueForm(forms.ModelForm):

    class Meta:
        model = Estoque
        fields = ('nf',)


class EstoqueItensEntradaForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'


class EstoqueItensSaidaForm(forms.ModelForm):

    class Meta:
        model = EstoqueItens
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstoqueItensSaidaForm, self).__init__(*args, **kwargs)
        # Retorna somente produtos com estoque maior do que zero.
        self.fields['produto'].queryset = Produto.objects.filter(estoque__gt=0)
