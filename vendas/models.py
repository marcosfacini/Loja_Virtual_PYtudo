from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produtos
from django.conf import settings

class Carrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produtos, related_name="adicionar_no_carrinho", blank=True)

    def __str__(self):
        return str(self.usuario)
