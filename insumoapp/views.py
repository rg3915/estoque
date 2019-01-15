from django.shortcuts import render, redirect
from .models import Produto, EntradaProduto
from .form import ProdutoForm, ProducaoForm


def index(request):
    data = {}
    data['produtos'] = Produto.objects.all()
    return render(request, 'insumoapp/index.html', data)


def sobre(request):
    return render(request, 'insumoapp/sobre.html')


def movimentos(request):
    data = {}
    data['produtos'] = EntradaProduto.objects.all()
    return render(request, 'insumoapp/movimentos.html', data)


def login(request):
    return render(request, 'insumoapp/login.html')


def controle(request):
    data = {}
    form = ProdutoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('index')

    data['form'] = form
    return render(request, 'insumoapp/controle.html', data)


def edit_prod(request, pk):
    # Efetua a edição dos produtos
    data = {}
    prod = Produto.objects.get(pk=pk)
    form = ProdutoForm(request.POST or None, instance=prod)

    if form.is_valid():
        form.save()
        return redirect('index')

    data['form'] = form
    return render(request, 'insumoapp/controle.html', data)


def entrada_prod(request):
    data = {}
    form = ProducaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('index')  # Verificar essa linha depois

    data['form'] = form
    return render(request, 'insumoapp/producao.html')
