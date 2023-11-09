from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria, DestacadosHome
from gestao.models import Banner
from vendas.models import ListaDesejo

def home(request):
    try:
        categorias = Categoria.objects.all()
    except:
        categorias = []
    try:
        produtos = DestacadosHome.objects.all()
    except:
        produtos = []
    banners = Banner.objects.filter(home=True)
    lista = ListaDesejo.objects.filter(usuario_id=request.user.id).first()
    num_lista_desejo = 0
    if lista:
        num_lista_desejo = lista.produtos.count()
    return render(request, 'home.html', {'categorias': categorias,
                                         'produtos': produtos,
                                         'banners': banners,
                                         'num_lista_desejo': num_lista_desejo})