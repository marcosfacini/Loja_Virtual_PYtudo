from django.db import models
from produtos.models import Produtos
from usuarios.models import Usuarios

class Pedido(models.Model):
    PARCELAS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ]

    STATUS = [
    ('WAITING', 'WAITING'),
    ('AUTHORIZED', 'AUTHORIZED'),
    ('IN_ANALYSIS', 'IN_ANALYSIS'),
    ('DECLINED', 'DECLINED'),
    ('PAID', 'PAID'),
    ('CANCELED', 'CANCELED'),
    ]

    METODO_DE_PAGAMENTO = [
    ('creditCard', 'creditCard'),
    ('boleto', 'boleto'),
    ('pix', 'pix'),
    ]

    parcelas = models.CharField(choices=PARCELAS, default='1', max_length=100)
    status = models.CharField(choices=STATUS, default='WAITING', max_length=100)
    produtos = models.ManyToManyField(Produtos, through='ItensPedido')
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_ultima_atualizacao_pedido = models.DateTimeField(auto_now=True, null=True)
    metodo_de_pagamento = models.CharField(choices=METODO_DE_PAGAMENTO, max_length=100)
    mensagem_de_erro = models.CharField(max_length=500, blank=True, null= True)

    def __str__(self):
        return str(self.id)

class ItensPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.SET_NULL, null=True)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return str(self.pedido)
