from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.urls import reverse
from django.views.generic import DetailView, ListView

from projeto.produto.models import Produto

from .forms import EstoqueForm, EstoqueItensEntradaForm, EstoqueItensSaidaForm
from .models import (
    Estoque,
    EstoqueEntrada,
    EstoqueItens,
    EstoqueSaida,
    ProtocoloEntrega
)


def estoque_entrada_list(request):
    template_name = 'estoque_list.html'
    objects = EstoqueEntrada.objects.all()
    context = {
        'object_list': objects,
        'titulo': 'Entrada',
        'url_add': 'estoque:estoque_entrada_add'
    }
    return render(request, template_name, context)


class EstoqueEntradaList(ListView):
    model = EstoqueEntrada
    template_name = 'estoque_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueEntradaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Entrada'
        context['url_add'] = 'estoque:estoque_entrada_add'
        return context


def estoque_entrada_detail(request, pk):
    template_name = 'estoque_detail.html'
    obj = EstoqueEntrada.objects.get(pk=pk)
    context = {
        'object': obj,
        'url_list': 'estoque:estoque_entrada_list'
    }
    return render(request, template_name, context)


class EstoqueDetail(DetailView):
    model = Estoque
    template_name = 'estoque_detail.html'


def dar_baixa_estoque(form):
    # Pega os produtos a partir da instância do formulário (Estoque).
    produtos = form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.estoque = item.saldo
        produto.save()
    print('Estoque atualizado com sucesso.')


def estoque_add(request, form_inline, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_formset = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form=form_inline,
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True,
    )
    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_form, prefix='main')
        formset = item_estoque_formset(
            request.POST,
            instance=estoque_form,
            prefix='estoque'
        )
        if form.is_valid() and formset.is_valid():
            form = form.save(commit=False)
            form.funcionario = request.user
            form.movimento = movimento
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            return {'pk': form.pk}
    else:
        form = EstoqueForm(instance=estoque_form, prefix='main')
        formset = item_estoque_formset(instance=estoque_form, prefix='estoque')
    context = {'form': form, 'formset': formset}
    return context


@login_required
def estoque_entrada_add(request):
    form_inline = EstoqueItensEntradaForm
    template_name = 'estoque_entrada_form.html'
    movimento = 'e'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, form_inline, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def estoque_saida_list(request):
    template_name = 'estoque_list.html'
    objects = EstoqueSaida.objects.all()
    context = {
        'object_list': objects,
        'titulo': 'Saída',
        'url_add': 'estoque:estoque_saida_add'
    }
    return render(request, template_name, context)


class EstoqueSaidaList(ListView):
    model = EstoqueSaida
    template_name = 'estoque_list.html'

    def get_context_data(self, **kwargs):
        context = super(EstoqueSaidaList, self).get_context_data(**kwargs)
        context['titulo'] = 'Saída'
        context['url_add'] = 'estoque:estoque_saida_add'
        return context


def estoque_saida_detail(request, pk):
    template_name = 'estoque_detail.html'
    obj = EstoqueSaida.objects.get(pk=pk)
    context = {
        'object': obj,
        'url_list': 'estoque:estoque_saida_list'
    }
    return render(request, template_name, context)


@login_required
def estoque_saida_add(request):
    form_inline = EstoqueItensSaidaForm
    template_name = 'estoque_saida_form.html'
    movimento = 's'
    url = 'estoque:estoque_detail'
    context = estoque_add(request, form_inline, template_name, movimento, url)
    if context.get('pk'):
        return HttpResponseRedirect(resolve_url(url, context.get('pk')))
    return render(request, template_name, context)


def protocolo_de_entrega(request):
    template_name = 'protocolo_de_entrega_list.html'
    objects = ProtocoloEntrega.objects.all()
    context = {
        'object_list': objects,
    }
    return render(request, template_name, context)


@login_required
def protocolo_de_entrega_detail(request, pk):
    template_name = 'protocolo_de_entrega_detail.html'
    obj = ProtocoloEntrega.objects.get(pk=pk)
    context = {
        'object': obj,
    }
    return render(request, template_name, context)


def dar_baixa_no_estoque_com_protocolo_de_entrega(request, pk):
    entrega = ProtocoloEntrega.objects.get(pk=pk)

    if entrega.estoque_atualizado:
        messages.error(request, 'Já foi dado baixa nessa entrega.')
        return HttpResponseRedirect(reverse('produto:produto_list'))

    # criar um Estoque saida
    estoque_saida = EstoqueSaida.objects.create(
        funcionario=request.user,
        movimento='s'
    )
    for item in entrega.protocolo_entrega.all():
        # Criar um Estoque Saida Detail
        EstoqueItens.objects.create(
            estoque=estoque_saida,
            produto=item.produto,
            quantidade=item.quantidade,
            saldo=item.produto.estoque - item.quantidade
        )
        # Dar baixa no estoque
        produtos = estoque_saida.estoques.all()
        for item_produto in produtos:
            produto = Produto.objects.get(pk=item_produto.produto.pk)
            produto.estoque = item_produto.saldo
            produto.save()
    entrega.estoque_atualizado = True
    entrega.save()
    messages.success(request, 'Estoque atualizado com sucesso.')
    return HttpResponseRedirect(reverse('produto:produto_list'))
