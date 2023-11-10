from django.contrib import admin
from .models import Categoria, Produtos, Imagens, Avaliacao, DestacadosHome, RegistroAlteracaoProduto

admin.site.register(Categoria)
admin.site.register(Produtos)
admin.site.register(Imagens)
admin.site.register(Avaliacao)
admin.site.register(DestacadosHome)
admin.site.register(RegistroAlteracaoProduto)
