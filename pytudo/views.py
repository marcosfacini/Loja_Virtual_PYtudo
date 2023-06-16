from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria, DestacadosHome
from gestao.models import Banner

def home(request):
    categorias = Categoria.objects.all()
    produtos = DestacadosHome.objects.all()
    try:
        banner = Banner.objects.get(home=True)
    except:
        banner = ''
    return render(request, 'home.html', {'categorias': categorias,
                                         'produtos': produtos,
                                         'banner': banner})