from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .models import Produtos, Categoria, Avaliacao
from .forms import CadastroProduto
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.decorators import has_permission_decorator, has_role_decorator
from django.db.models import Q
from decimal import Decimal



def listar_produtos(request):
    produtos = Produtos.objects.all()
    categorias = Categoria.objects.all()
    nome_filtrar = request.GET.get('nome')
    categoria_filtrar = request.GET.get('categoria')
    if nome_filtrar or categoria_filtrar:
        if categoria_filtrar == None:
            produtos = produtos.filter(nome__icontains=nome_filtrar)
        else:
            produtos = produtos.filter(nome__icontains=nome_filtrar).filter(categoria_id=categoria_filtrar)
    return render(request, 'produtos.html', {'produtos': produtos, 
                                            'categorias': categorias})

@has_permission_decorator('alterar_produto')
def cadastrar_produto(request):
    if request.method == 'POST':
        formulario = CadastroProduto(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.add_message(request, constants.SUCCESS, 'Produto salvo com sucesso.')
            return redirect('/produtos/listar_produtos')
        else:
            messages.add_message(request, constants.ERROR, 'Erro ao salvar formulário. Tente novamente.')
            return redirect('/produtos/cadastrar_produto')
    else:
        form = CadastroProduto()
        return render(request, 'cadastrar_produto.html', {'form': form})

def ver_produto(request, id):
    produto = Produtos.objects.get(id=id)
    avaliacoes = Avaliacao.objects.filter(produto=id)
    print (avaliacoes)
    return render(request, 'ver_produto.html', {'produto': produto,
                                                'avaliacoes': avaliacoes})

@has_permission_decorator('alterar_produto')
def excluir_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    return redirect('/produtos/listar_produtos')

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

@has_permission_decorator('alterar_produto')
def cadastrar_categoria(request):
    nome = request.POST.get('nome')
    categoria = Categoria(nome=nome)
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria salva com sucesso.')
    return redirect('/produtos/listar_categorias')

@has_permission_decorator('alterar_produto')
def excluir_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    messages.add_message(request, constants.SUCCESS, 'Categoria excluída com sucesso.')
    return redirect('/produtos/listar_categorias')

@has_permission_decorator('alterar_produto')
def alterar_produto(request, id):
    if request.method == 'GET':
        produto = Produtos.objects.get(id=id)
        categorias = Categoria.objects.all()
        return render(request, 'alterar_produto.html', {'produto': produto,
                                                        'categorias': categorias})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        produto = Produtos.objects.get(id=id)
        categoria_by_id = Categoria.objects.get(id=categoria)
        produto.nome = nome
        produto.descricao = descricao
        preco_in_decimal = Decimal(preco.replace(',','.'))
        produto.preco = preco_in_decimal
        produto.categoria = categoria_by_id
        produto.quantidade = quantidade
        produto.save()
        messages.add_message(request, constants.SUCCESS, 'Produto atualizado com sucesso.')
        return redirect(f'/produtos/alterar_produto/{id}')
    
def salvar_avaliacao(request, id_produto):
    estrelas = request.POST.get('estrelas')
    comentario = request.POST.get('comentario')
    avalicao = Avaliacao(usuario=request.user, produto_id=id_produto, estrelas=estrelas, comentario=comentario)
    avalicao.save()
    return redirect(f'/produtos/ver_produto/{id_produto}')

