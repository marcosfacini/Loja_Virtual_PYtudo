from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import Carrinho
from django.urls import reverse

def vender_produto(request, id):
    produto = Produtos.objects.get(id=id)
    unidades_vendidas = int(request.POST.get('quantidade'))
    produto.quantidade  = produto.quantidade - unidades_vendidas
    produto.save()
    return redirect(f'/produtos/ver_produto/{id}')

def adicionar_no_carrinho(request, id):
    carrinho_existente = Carrinho.objects.filter(usuario=request.user.id).first()
    produto = Produtos.objects.get(id=id)
    if carrinho_existente:
        carrinho_existente.produtos.add(produto) 
        return redirect(reverse('ver_carrinho'))
    else:
        carrinho = Carrinho(usuario_id=request.user.id) 
        carrinho.save()
        carrinho.produtos.add(produto)
        return redirect(reverse('ver_carrinho'))

def ver_carrinho(request):
    carrinho = Carrinho.objects.filter(usuario=request.user.id).first()
    return render(request, 'ver_carrinho.html', {'carrinho': carrinho})


def esvaziar_carrinho(request):
    carrinho = Carrinho.objects.filter(usuario=request.user.id).first()
    if carrinho:
        carrinho.delete()
        return redirect(reverse('listar_produtos'))
    else:
        return redirect(reverse('ver_carrinho'))


