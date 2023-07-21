from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import ListaDesejo, Venda, ItemVenda
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants 
from django.contrib.auth.decorators import login_required
from .forms import CupomDesconto

@login_required
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

def excluir_item_da_lista(request, id_produto):
    lista = ListaDesejo.objects.get(usuario_id=request.user.id)
    produto = Produtos.objects.get(id=id_produto)
    lista.produtos.remove(produto)
    return redirect('ver_lista_desejo')

def esvaziar_lista_desejo(request):
    try:
        lista = ListaDesejo.objects.get(usuario=request.user.id)
        lista.delete()
    except:
        messages.add_message(request, constants.ERROR, 'Erro ao deletar ou a lista já está vazia')
    return redirect(reverse('ver_lista_desejo'))


def adicionar_ao_carrinho(request, produto_id):
    if 'carrinho' not in request.session:
        request.session['carrinho'] = {}

    carrinho = request.session['carrinho']
    id_produto = str(produto_id)
    if id_produto in carrinho:
        carrinho[id_produto] += 1
    else:
        carrinho[id_produto] = 1
    request.session.modified = True

    return redirect('carrinho')

def remover_do_carrinho(request, produto_id):
    if 'carrinho' in request.session:
        carrinho = request.session['carrinho']
        id_produto = str(produto_id)
        if id_produto in carrinho:
            carrinho[id_produto] -= 1
            if carrinho[id_produto] <= 0:
                del carrinho[id_produto]
            request.session.modified = True

    return redirect('carrinho')

def carrinho(request):
    carrinho = []
    total = 0

    if 'carrinho' in request.session:
        carrinho_session = request.session['carrinho']
        carrinho_ids = list(carrinho_session.keys())
        carrinho = Produtos.objects.filter(id__in=carrinho_ids)
        soma_unidades = []
        for produto in carrinho:
            soma = produto.preco * carrinho_session[str(produto.id)]
            soma_unidades.append(soma)
        total = sum(soma_unidades)

    return render(request, 'carrinho.html', {'carrinho': carrinho, 'total': total})

def adicionar_quantidade_no_carrinho(request):
    carrinho = request.session['carrinho']
    for key, value in request.POST.items():
        if key.startswith('quantidade_') and value != '':
            replace = key.replace('quantidade_', '')
            carrinho[replace] = int(value)
            request.session.modified = True
    return redirect('carrinho')

def excluir_do_carrinho(request, id_produto):
    carrinho = request.session['carrinho']
    del carrinho[str(id_produto)]
    request.session.modified = True
    return redirect('carrinho')

def criar_cupom(request):
    if request.method == 'POST':
        form = CupomDesconto(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Cupom criado com sucesso.')
            return redirect('gerenciar_cupons')
        else:
            messages.add_message(request, constants.ERROR, 'Não foi possível criar o cupom.')
    else:
        form = CupomDesconto()
    return render(request, 'criar_cupom.html', {'form': form})


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


