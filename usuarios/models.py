from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from cpf_field.models import CPFField

class Usuarios(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    cpf = CPFField('CPF')
    data_de_nascimento = models.DateField(default=None, null=True) # tirar null=True
    celular = PhoneNumberField(null=False, blank=False)
    endereco = models.CharField(max_length=50)
    numero_endereco = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null= True)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return str(self.usuario)


