from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import ListaDesejo, Venda, ItemVenda
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants 

def adicionar_na_lista_desejo(request, id):
    lista_existente = ListaDesejo.objects.filter(usuario=request.user.id).first()
    produto = Produtos.objects.get(id=id)
    if lista_existente:
        lista_existente.produtos.add(produto) 
        return redirect(reverse('ver_lista_desejo'))
    else:
        lista = ListaDesejo(usuario_id=request.user.id) 
        lista.save()
        lista.produtos.add(produto)
        return redirect(reverse('ver_lista_desejo'))

def ver_lista_desejo(request):
    lista = ListaDesejo.objects.filter(usuario_id=request.user.id).first()
    return render(request, 'ver_lista_desejo.html', {'lista': lista})


def esvaziar_lista_desejo(request):
    try:
        lista = ListaDesejo.objects.get(usuario=request.user.id)
        lista.delete()
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao deletar ou a lista já está vazia')
    return redirect(reverse('ver_lista_desejo'))


def adicionar_ao_carrinho(request, produto_id):
    produto = Produtos.objects.get(id=produto_id)

    if 'carrinho' not in request.session:
        request.session['carrinho'] = []

    carrinho = request.session['carrinho']
    carrinho.append(produto.id)
    request.session.modified = True

    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    produto = Produtos.objects.get(id=produto_id)

    carrinho = request.session.get('carrinho', [])
    if produto.id in carrinho:
        carrinho.remove(produto.id)
        request.session.modified = True

    return redirect('carrinho')

def carrinho(request):
    carrinho = []
    total = 0

    if 'carrinho' in request.session:
        carrinho_ids = request.session['carrinho']
        carrinho = Produtos.objects.filter(id__in=carrinho_ids)
        total = sum(produto.preco for produto in carrinho)

    return render(request, 'carrinho.html', {'carrinho': carrinho,'total': total})


def vender_produto(request, id):
    produto = Produtos.objects.get(id=id)
    unidades_vendidas = int(request.POST.get('quantidade'))
    produto.quantidade  = produto.quantidade - unidades_vendidas
    produto.save()
    return redirect(f'/produtos/ver_produto/{id}')

def criar_historico_da_venda(request, produtos_ids, quantidades, valor_total):
    venda = Venda(usuario=request.user.id, valor_total=valor_total)
    venda.save()
    for produto_id, quantidade in zip(produtos_ids, quantidades):
        ItemVenda.objects.create(venda=venda, produto=produto_id, quantidade=int(quantidade))


