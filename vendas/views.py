from django.shortcuts import render, redirect
from produtos.models import Produtos

def vender_produto(request, id):
    produto = Produtos.objects.get(id=id)
    unidades_vendidas = int(request.POST.get('quantidade'))
    produto.quantidade  = produto.quantidade - unidades_vendidas
    produto.save()
    return redirect(f'/produtos/ver_produto/{id}')
