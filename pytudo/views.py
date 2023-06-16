from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria, DestacadosHome
from gestao.models import Banner

def home(request):
    categorias = Categoria.objects.all()
    produtos = DestacadosHome.objects.all()
    banners = Banner.objects.filter(home=True)
    return render(request, 'home.html', {'categorias': categorias,
                                         'produtos': produtos,
                                         'banners': banners})