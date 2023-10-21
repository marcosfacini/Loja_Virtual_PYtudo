from typing import Any, Dict, Tuple
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuarios.models import Usuarios
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class Categoria(models.Model):
    nome = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

class Produtos(models.Model):
    nome = models.CharField(max_length=40)
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
    especificacao = RichTextUploadingField(blank=True, null=True)


    def __str__(self):
        return self.nome
    
    def delete(self, *args, **kwargs):
        registro = RegistroAlteracaoProduto(
            produto=self,
            detalhes=f'Produto {self.nome} excluído.',
        )
        registro.save()
        super().delete(*args, **kwargs)
        
    
    def save(self, *args, **kwargs):
        if self.data_cadastro != self.data_atualizacao:
            old_obj = Produtos.objects.get(pk=self.pk)
            old_nome = old_obj.nome
            old_descricao = old_obj.descricao
            old_preco_de_custo = old_obj.preco_de_custo
            old_preco = old_obj.preco
            old_categoria = old_obj.categoria
            old_marca = old_obj.marca
            old_cor = old_obj.cor
            old_quantidade = old_obj.quantidade
            old_imagem_principal = old_obj.imagem_principal
            old_especificacao = old_obj.especificacao
            detalhes = f"Produto atualizado - {self.comparar_alteracoes(old_nome, old_descricao, old_preco_de_custo, old_preco, old_categoria, old_marca, old_cor, old_quantidade, old_imagem_principal, old_especificacao)}"
        else:
            detalhes = f"Produto {self.nome} criado"

        super().save(*args, **kwargs)
            
        registro = RegistroAlteracaoProduto(
            produto=self,
            detalhes=detalhes,
        )
        registro.save()

    def comparar_alteracoes(self, old_nome, old_descricao, old_preco_de_custo, old_preco, old_categoria, old_marca, old_cor, old_quantidade, old_imagem_principal, old_especificacao):
        alteracoes = []

        if old_nome != self.nome:
            alteracoes.append(f"Nome alterado de '{old_nome}' para '{self.nome}'")

        if old_descricao.strip() != self.descricao.strip():
            alteracoes.append("Descrição alterada")

        if old_preco_de_custo != self.preco_de_custo:
            alteracoes.append(f"Preço de custo alterado de '{old_preco_de_custo}' para '{self.preco_de_custo}'")

        if old_preco != self.preco:
            alteracoes.append(f"Preço alterado de '{old_preco}' para '{self.preco}'")

        if old_categoria != self.categoria:
            alteracoes.append(f"Categoria alterada de '{old_categoria}' para '{self.categoria}'")

        if old_marca != self.marca:
            alteracoes.append(f"Marca alterada de '{old_marca}' para '{self.marca}'")

        if old_cor != self.cor:
            alteracoes.append(f"Cor alterada de '{old_cor}' para '{self.cor}'")

        if old_quantidade != int(self.quantidade):
            alteracoes.append(f"Quantidade alterada de '{old_quantidade}' para '{self.quantidade}'")

        if old_imagem_principal != self.imagem_principal:
            alteracoes.append(f"Imagem principal alterada de '{old_imagem_principal}' para '{self.imagem_principal}'")

        if old_especificacao != self.especificacao:
            alteracoes.append(f"As especificações foram alteradas")


        return ", ".join(alteracoes)
    
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
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    estrelas = models.CharField(max_length=1, choices=choices)
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.usuario
    
class DestacadosHome(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)

    def __str__(self):
        return self.produto.nome
    

class RegistroAlteracaoProduto(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.SET_NULL, null=True)
    data_atualizacao = models.DateTimeField(default=timezone.now)
    detalhes = models.TextField()

    def __str__(self):
        return f"{self.produto.nome} - {self.data_atualizacao}"


