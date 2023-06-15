from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria, DestacadosHome

def home(request):
    categorias = Categoria.objects.all()
    produtos = DestacadosHome.objects.all()
    return render(request, 'home.html', {'categorias': categorias,
                                         'produtos': produtos})