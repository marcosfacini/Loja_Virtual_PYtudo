from django.db import models
from produtos.models import Produtos
from checkout.models import Pedido
from django.conf import settings

class ListaDesejo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produtos, related_name="produtos", blank=True)

    def __str__(self):
        return str(self.usuario)

class CupomDesconto(models.Model):
    choices = (('P', 'Porcentagem'),('R', 'Reais'))
    codigo = models.CharField(max_length=50, unique=True)
    tipo_desconto = models.CharField(max_length=1, choices=choices)
    desconto = models.FloatField()
    quantidade = models.PositiveIntegerField()
    inicio_validade = models.DateField()
    fim_validade = models.DateField()
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo
    
class HistoricoCupomDesconto(models.Model):
    venda = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.venda.id} - {self.data}"
