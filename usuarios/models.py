from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# TODO campo celular/numero_endereco/cpf serão charfield mesmo? como serao validados? migrações não foram feitas ainda para esses campos
class Usuarios(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=40)
    # cpf = models.CharField(max_length=11)
    celular = models.CharField(max_length=15)
    endereco = models.CharField(max_length=50)
    numero_endereco = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)

    def __str__(self):
        return str(self.usuario)


