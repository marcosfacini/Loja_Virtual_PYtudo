from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuarios.models import Usuarios

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
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    estrelas = models.CharField(max_length=1, choices=choices)
    comentario = models.TextField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.comentario
    
class DestacadosHome(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)

    def __str__(self):
        return self.produto.nome
    
class Banner(models.Model):
    imagem = models.ImageField(upload_to ='banners/')

