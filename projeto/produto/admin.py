import csv
from datetime import datetime

import xlwt
from django.contrib import admin
from django.http import HttpResponse

from .models import Categoria, Produto

MDATA = datetime.now().strftime('%Y-%m-%d')


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'importado',
        'ncm',
        'preco',
        'estoque',
        'estoque_minimo',
        'categoria',
    )
    search_fields = ('produto',)
    list_filter = ('importado',)
    actions = ('export_as_csv', 'export_as_xlsx')

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.3.1.min.js',
            '/static/js/estoque_admin.js'
        )

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Exportar CSV"

    def export_as_xlsx(self, request, queryset):

        meta = self.model._meta
        columns = (
            'Importado',
            'NCM',
            'Produto',
            'Preço',
            'Estoque',
            'Estoque mínimo',
            'Categoria'
        )

        response = HttpResponse(content_type='application/ms-excel')
        response[
            'Content-Disposition'] = 'attachment; filename="%s_%s.xlsx"' % (meta, MDATA)

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(self.model.__name__)

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        default_style = xlwt.XFStyle()

        rows = queryset.values_list(
            'importado',
            'ncm',
            'produto',
            'preco',
            'estoque',
            'estoque_minimo',
            'categoria__categoria',
        )
        for row, rowdata in enumerate(rows):
            row_num += 1
            for col, val in enumerate(rowdata):
                ws.write(row_num, col, val, default_style)

        wb.save(response)
        return response

    export_as_xlsx.short_description = "Exportar XLSX"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    search_fields = ('categoria',)
