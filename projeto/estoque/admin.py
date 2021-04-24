from django.contrib import admin

from .models import (
    EstoqueEntrada,
    EstoqueItens,
    EstoqueSaida,
    ProtocoloEntrega,
    ProtocoloEntregaItens
)


class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0


@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'


@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario',)
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created'


class ProtocoloEntregaItensInline(admin.TabularInline):
    model = ProtocoloEntregaItens
    extra = 0


@admin.register(ProtocoloEntrega)
class ProtocoloEntregaAdmin(admin.ModelAdmin):
    inlines = (ProtocoloEntregaItensInline,)
    list_display = ('__str__', 'estoque_atualizado')
    list_filter = ('usuario',)
    date_hierarchy = 'created'
