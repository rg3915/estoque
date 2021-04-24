import csv
import io
from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView

from projeto.produto.actions.export_xlsx import export_xlsx
from projeto.produto.actions.import_xlsx import \
    import_xlsx as action_import_xlsx

from .forms import ProdutoForm
from .models import Produto


def produto_list(request):
    template_name = 'produto_list.html'
    objects = Produto.objects.all()
    search = request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list': objects}
    return render(request, template_name, context)


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super(ProdutoList, self).get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(produto__icontains=search) |
                Q(ncm__icontains=search)
            )
        return queryset


def produto_detail(request, pk):
    template_name = 'produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def produto_add(request):
    form = ProdutoForm(request.POST or None)
    template_name = 'produto_form2.html'

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('produto:produto_list'))

    context = {'form': form}
    return render(request, template_name, context)


class ProdutoCreate(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm


def produto_json(request, pk):
    ''' Retorna o produto, id e estoque. '''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data': data})


def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        produto = item.get('produto')
        ncm = str(item.get('ncm'))
        importado = True if item.get('importado') == 'True' else False
        preco = item.get('preco')
        estoque = item.get('estoque')
        estoque_minimo = item.get('estoque_minimo')
        obj = Produto(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)


def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # Lendo arquivo InMemoryUploadedFile
        file = myfile.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))
        # Gerando uma list comprehension
        data = [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('produto:produto_list'))

    template_name = 'produto_import.html'
    return render(request, template_name)


def export_csv(request):
    header = (
        'importado', 'ncm', 'produto', 'preco', 'estoque', 'estoque_minimo',
    )
    produtos = Produto.objects.all().values_list(*header)
    with open('fix/produtos_exportados.csv', 'w') as csvfile:
        produto_writer = csv.writer(csvfile)
        produto_writer.writerow(header)
        for produto in produtos:
            produto_writer.writerow(produto)
    messages.success(request, 'Produtos exportados com sucesso.')
    return HttpResponseRedirect(reverse('produto:produto_list'))


def import_xlsx(request):
    filename = 'fix/produtos.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Produtos importados com sucesso.')
    return HttpResponseRedirect(reverse('produto:produto_list'))


def exportar_produtos_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Produto'
    filename = 'produtos_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Produto.objects.all().values_list(
        'importado',
        'ncm',
        'produto',
        'preco',
        'estoque',
        'estoque_minimo',
        'categoria__categoria',
    )
    columns = ('Importado', 'NCM', 'Produto', 'Preço',
               'Estoque', 'Estoque mínimo', 'Categoria')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response


def import_csv_with_pandas(request):
    filename = 'fix/produtos.csv'
    df = pd.read_csv(filename)
    aux = []
    for row in df.values:
        obj = Produto(
            produto=row[0],
            ncm=row[1],
            importado=row[2],
            preco=row[3],
            estoque=row[4],
            estoque_minimo=row[5],
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)
    messages.success(request, 'Produtos importados com sucesso.')
    return HttpResponseRedirect(reverse('produto:produto_list'))
