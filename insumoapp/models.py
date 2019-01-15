from django.db import models


class Produto(models.Model):
    # Dados dos materiais(Durex,Caixa de papelão etc) de insumo.
    codigo = models.IntegerField(primary_key=True, blank=False, null=False)
    descricao = models.CharField(max_length=100, blank=False, null=False)
    tipo = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.descricao


class EntradaProduto(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    prod = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    qtd = models.IntegerField(blank=False, null=False)
    dt_mov = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tip = models.CharField(max_length=10, default='entrada')

    def __str__(self):
        return str(self.prod.descricao)

        # return '{} - {}'.format(str(self.prod.descricao), self.qtd)


class SaidaProduto(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    prod = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    qtd = models.IntegerField(blank=False, null=False)
    dt_mov = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tip = models.CharField(max_length=10, default='saida')


'''
class Producao(models.Model):
    # Dados para Entrada e Saída de materiais(Durex,Caixa de papelão etc).
    descricao = models.CharField(max_length=100, blank=False, null=False)
    qtd = models.IntegerField(blank=False, null=False)
    dt_mov = models.DateTimeField(auto_now_add=True)
    # Mostrar o usuario que vai dar Entrada ou Saída
    # entrada = models.models.CharField(default='entrada')

    def __str__(self):
        return self.descricao

'''
