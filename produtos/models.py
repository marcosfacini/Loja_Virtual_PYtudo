from django.db import models

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
