from django.shortcuts import render, redirect
from django.contrib import messages
from produtos.models import Categoria

def home(request):
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'categorias': categorias})