from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Categoria(models.Model):
    nome = models.CharField(max_length=40)


    def __str__(self):
        return self.nome

class Produtos(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    foto = models.ImageField()
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome
    
class Avaliacao(models.Model):
    choices = (
        ('1', 'Pessimo'),
        ('2', 'Ruim'),
        ('3', 'Bom'),
        ('4', 'Otimo'),
        ('5', 'Perfeito')
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    estrelas = models.CharField(max_length=1, choices=choices, blank=True, null=True)
    comentario = models.TextField()

    def __str__(self):
        return self.estrelas
