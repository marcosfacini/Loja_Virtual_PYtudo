from django.db import models

class Banner(models.Model):
    imagem = models.ImageField(upload_to ='banners/')
    home = models.BooleanField(default=False)
