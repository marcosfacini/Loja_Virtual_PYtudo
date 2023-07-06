from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import ListaDesejo, Venda, ItemVenda
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants 

def vender_produto(request, id):
    produto = Produtos.objects.get(id=id)
    unidades_vendidas = int(request.POST.get('quantidade'))
    produto.quantidade  = produto.quantidade - unidades_vendidas
    produto.save()
    return redirect(f'/produtos/ver_produto/{id}')

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
   
    
def criar_historico_da_venda(request, produtos_ids, quantidades, valor_total):
    venda = Venda(usuario=request.user.id, valor_total=valor_total)
    venda.save()
    for produto_id, quantidade in zip(produtos_ids, quantidades):
        ItemVenda.objects.create(venda=venda, produto=produto_id, quantidade=int(quantidade))


