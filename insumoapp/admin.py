from django.contrib import admin
from .models import Produto, EntradaProduto, SaidaProduto


class CamposAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'qtd', 'tip', 'dt_mov')


admin.site.register(Produto)
admin.site.register(EntradaProduto, CamposAdmin)
admin.site.register(SaidaProduto)
