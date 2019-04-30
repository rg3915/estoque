from django.db import models


class EstoqueEntradaManager(models.Manager):

    def get_queryset(self):
        return super(EstoqueEntradaManager, self).get_queryset().filter(movimento='e')


class EstoqueSaidaManager(models.Manager):

    def get_queryset(self):
        return super(EstoqueSaidaManager, self).get_queryset().filter(movimento='s')
