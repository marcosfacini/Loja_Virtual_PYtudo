from django.db import models

class Banner(models.Model):
    imagem = models.ImageField(upload_to ='banners/')
    home = models.BooleanField(default=False)
    titulo = models.CharField(max_length=50, blank=True, null=True)
    subtitulo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.imagem}"
