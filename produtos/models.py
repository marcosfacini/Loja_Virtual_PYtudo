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
    preco_de_custo = models.DecimalField(max_digits=8, decimal_places=2)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.SET_NULL)
    marca = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=30, blank=True, null=True)
    quantidade = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True)
    imagem_principal = models.ImageField(upload_to ='produtos/', blank=True, null=True)


    def __str__(self):
        return self.nome
    
class Imagens(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE) 
    foto = models.ImageField(upload_to ='produtos/')
    
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
