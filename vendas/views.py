from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import ListaDesejo, Venda, ItemVenda
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants 
from django.contrib.auth.decorators import login_required
from .forms import FormCupomDesconto
from .models import CupomDesconto 
from datetime import date

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
    total_com_desconto = None

    if 'carrinho' in request.session:
        carrinho_session = request.session['carrinho']
        carrinho_ids = list(carrinho_session.keys())
        carrinho = Produtos.objects.filter(id__in=carrinho_ids)
        soma_unidades = []
        unidades = []
        for produto in carrinho:
            soma = produto.preco * carrinho_session[str(produto.id)]
            soma_unidades.append(soma)
            unidades.append(carrinho_session[str(produto.id)])
        total = sum(soma_unidades)
        total_unidades = sum(unidades)

    if 'cupom' in request.session:
        cupom = request.session['cupom']
        valor_desconto = cupom['desconto'][0]
        tipo_desconto = cupom['desconto'][1]
        if tipo_desconto == 'R':
            total_com_desconto = float(total) - valor_desconto
            if total_com_desconto <= 0:
                total_com_desconto = 0
        elif tipo_desconto == 'P':
            total_com_desconto = float(total) - (float(total) * valor_desconto / 100)
            if total_com_desconto <= 0:
                total_com_desconto = 0

    return render(request, 'carrinho.html', {'carrinho': carrinho, 
                                             'total': total, 
                                             'total_com_desconto': total_com_desconto,
                                             'total_unidades': total_unidades})

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
        form = FormCupomDesconto(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Cupom criado com sucesso.')
            return redirect('gerenciar_cupons')
        else:
            messages.add_message(request, constants.ERROR, 'Não foi possível criar o cupom.')
    else:
        form = FormCupomDesconto()
    return render(request, 'criar_cupom.html', {'form': form})

def validar_cupom(request):
    codigo = request.POST.get('codigo')
    dia_atual = date.today()
    try:
        cupom = CupomDesconto.objects.get(codigo=codigo)
    except:
        messages.add_message(request, constants.ERROR, 'Cupom inválido.')
        return redirect('carrinho')
    if cupom.quantidade < 1:
        messages.add_message(request, constants.ERROR, 'Cupom esgotado.')
        return redirect('carrinho')
    if cupom.ativo == False:
        messages.add_message(request, constants.ERROR, 'Cupom desativado.')
        return redirect('carrinho')
    if cupom.inicio_validade > dia_atual:
        messages.add_message(request, constants.ERROR, 'Cupom fora da validade.')
        return redirect('carrinho')
    if dia_atual > cupom.fim_validade:
        messages.add_message(request, constants.ERROR, 'Cupom fora do prazo de validade.')
        return redirect('carrinho')
    
    request.session['cupom'] = {}
    desconto = request.session['cupom']
    desconto['desconto'] = [cupom.desconto, cupom.tipo_desconto]
    request.session.modified = True
    
    messages.add_message(request, constants.SUCCESS, f'Cupom {cupom.codigo} adicionado.')
    return redirect('carrinho')

def retirar_cupom_da_session(request):
    if 'cupom' in request.session:
        del request.session['cupom']
        request.session.modified = True
        messages.add_message(request, constants.SUCCESS, f'Cupom removido.')
    return redirect('carrinho')
    

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


