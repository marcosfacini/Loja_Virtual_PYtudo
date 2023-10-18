from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria, DestacadosHome
from gestao.models import Banner
from vendas.models import ListaDesejo

def home(request):
    categorias = Categoria.objects.all()
    produtos = DestacadosHome.objects.all()
    banners = Banner.objects.filter(home=True)
    lista = ListaDesejo.objects.filter(usuario_id=request.user.id).first()
    num_lista_desejo = 0
    if lista:
        num_lista_desejo = lista.produtos.count()
    return render(request, 'home.html', {'categorias': categorias,
                                         'produtos': produtos,
                                         'banners': banners,
                                         'num_lista_desejo': num_lista_desejo})