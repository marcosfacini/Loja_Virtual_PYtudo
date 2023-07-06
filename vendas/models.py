from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produtos
from django.conf import settings

class ListaDesejo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produtos, related_name="produtos", blank=True)

    def __str__(self):
        return str(self.usuario)
    
class Venda(models.Model):
    produtos = models.ManyToManyField(Produtos, through='ItemVenda')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.valor_total)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.SET_NULL, null=True)
    quantidade = models.PositiveIntegerField()
