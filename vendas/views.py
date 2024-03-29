from django.shortcuts import render, redirect
from produtos.models import Produtos
from vendas.models import ListaDesejo
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.decorators import has_role_decorator
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

@login_required
def ver_lista_desejo(request):
    lista = ListaDesejo.objects.filter(usuario_id=request.user.id).first()
    num_lista_desejo = 0
    if lista:
        num_lista_desejo = lista.produtos.count()
    return render(request, 'ver_lista_desejo.html', {'lista': lista, 'num_lista_desejo': num_lista_desejo})

@login_required
def excluir_item_da_lista(request, id_produto):
    lista = ListaDesejo.objects.get(usuario_id=request.user.id)
    produto = Produtos.objects.get(id=id_produto)
    lista.produtos.remove(produto)
    return redirect('ver_lista_desejo')

@login_required
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

    if 'carrinho' in request.session:
        carrinho_session = request.session['carrinho']
        carrinho_ids = list(carrinho_session.keys())
        carrinho = Produtos.objects.filter(id__in=carrinho_ids)
        soma_unidades = []
        for produto in carrinho:
            soma = produto.preco * carrinho_session[str(produto.id)]
            soma_unidades.append(soma)
        total = sum(soma_unidades)
        request.session['total'] = round(float(total), 2)
        request.session.modified = True
 
    if 'cupom' in request.session:
        cupom = request.session['cupom']
        valor_desconto = cupom['desconto'][0]
        tipo_desconto = cupom['desconto'][1]
        if tipo_desconto == 'R':
            total_com_desconto = float(total) - valor_desconto
            if total_com_desconto <= 0:
                total_com_desconto = 0
        elif tipo_desconto == 'P':
            total_com_desconto = round(float(total) - (float(total) * valor_desconto / 100),2)
            if total_com_desconto <= 0:
                total_com_desconto = 0
        request.session['total_com_desconto'] = round(float(total_com_desconto), 2)
        request.session.modified = True

    return render(request, 'carrinho.html', {'carrinho': carrinho})

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

@has_role_decorator('gerente')
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
    desconto['desconto'] = [cupom.desconto, cupom.tipo_desconto, cupom.id]
    request.session.modified = True
    
    messages.add_message(request, constants.SUCCESS, f'Cupom {cupom.codigo} adicionado.')
    return redirect('carrinho')

def retirar_cupom_da_session(request):
    if 'cupom' in request.session:
        del request.session['cupom']
        request.session.modified = True
        messages.add_message(request, constants.SUCCESS, f'Cupom removido.')
    return redirect('carrinho')
    


