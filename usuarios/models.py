from django.db import models

class Usuarios(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=35)
    senha = models.CharField(max_length=64)
    celular = models.CharField(max_length=15)
    endereco = models.CharField(max_length=50)
    numero_endereco = models.CharField(max_length=10)
    bairro = models.CharField(max_length=30)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)

    def __str__(self):
        return self.nome


