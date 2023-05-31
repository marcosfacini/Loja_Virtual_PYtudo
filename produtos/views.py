from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from .models import Produtos, Categoria, Avaliacao, Imagens
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.decorators import has_permission_decorator, has_role_decorator
from decimal import Decimal
from django.core.paginator import Paginator



def listar_produtos(request):
    produtos = Produtos.objects.all()
    categorias = Categoria.objects.all()
    
    nome_filtrar = request.GET.get('nome')
    if nome_filtrar:
        produtos = produtos.filter(nome__icontains=nome_filtrar)
    
    categoria_filtrar = request.GET.get('categoria')
    if categoria_filtrar: 
        produtos = produtos.filter(categoria_id=categoria_filtrar)
    
    preco_menor_filtrar = request.GET.get('preco_menor_filtrar')
    if preco_menor_filtrar:
        preco_menor_filtrar_decimal = Decimal(preco_menor_filtrar.replace(',','.'))
        produtos = produtos.filter(preco__lt=preco_menor_filtrar_decimal)
    
    preco_maior_filtrar = request.GET.get('preco_maior_filtrar')
    if preco_maior_filtrar:
        preco_maior_filtrar_decimal = Decimal(preco_maior_filtrar.replace(',','.'))
        produtos = produtos.filter(preco__gt=preco_maior_filtrar_decimal)

    marca_filtar = request.GET.get('marca')
    if marca_filtar:
        produtos = produtos.filter(marca__icontains=marca_filtar)

    cor_filtar = request.GET.get('cor')
    if cor_filtar:
        produtos = produtos.filter(cor__icontains=cor_filtar)

    produtos_ordenados = produtos.order_by('-id')
    paginacao = Paginator(produtos_ordenados, 3)

    ordenacao = request.GET.get('ordenacao')
    if ordenacao == 'maior':
        produtos_ordenados = produtos.order_by('-preco')
        paginacao = Paginator(produtos_ordenados, 3)

    elif ordenacao == 'menor':
        produtos_ordenados = produtos.order_by('preco')
        paginacao = Paginator(produtos_ordenados, 3)
    
    page = request.GET.get('page')
    produtos_paginados = paginacao.get_page(page)

    return render(request, 'produtos.html', {'produtos_paginados': produtos_paginados, 
                                             'categorias': categorias,})

@has_permission_decorator('alterar_produto')
def cadastrar_produto(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco_de_custo = request.POST.get('preco_de_custo')
        preco_de_custo_in_decimal = Decimal(preco_de_custo.replace(',','.'))
        preco = request.POST.get('preco')
        preco_in_decimal = Decimal(preco.replace(',','.'))
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        cor = request.POST.get('cor')
        quantidade = request.POST.get('quantidade')
        imagem_principal = request.FILES.get('imagem_principal')

        produto = Produtos(nome=nome, 
                           descricao=descricao, 
                           preco_de_custo=preco_de_custo_in_decimal, 
                           preco=preco_in_decimal, 
                           categoria_id=categoria, 
                           marca=marca, 
                           cor=cor, 
                           quantidade=quantidade)
        produto.save()

        imagens = request.FILES.getlist('imagens')
        if imagens:
            for img in imagens:
                imagem = Imagens(produto=produto, foto=img)
                imagem.save()
        messages.add_message(request, constants.SUCCESS, 'Produto salvo com sucesso.')
        # TODO fazer logica de mensagens de erro e de validaçoes do form

    return render(request, 'cadastrar_produto.html', {'categorias': categorias})

def ver_produto(request, id):
    produto = Produtos.objects.get(id=id)
    avaliacoes = Avaliacao.objects.filter(produto=id)
    imagens = Imagens.objects.filter(produto_id=id)
    return render(request, 'ver_produto.html', {'produto': produto,
                                                'avaliacoes': avaliacoes,
                                                'imagens': imagens})

@has_permission_decorator('alterar_produto')
def excluir_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    messages.add_message(request, constants.SUCCESS, 'Produto excluído com sucesso.')
    return redirect('/gestao/adm_estoque')

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
        imagens = Imagens.objects.filter(produto_id=id)
        return render(request, 'alterar_produto.html', {'produto': produto,
                                                        'categorias': categorias,
                                                        'imagens': imagens})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco_de_custo = request.POST.get('preco_de_custo')
        preco = request.POST.get('preco')
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        cor = request.POST.get('cor')
        quantidade = request.POST.get('quantidade')
        produto = Produtos.objects.get(id=id)
        categoria_by_id = Categoria.objects.get(id=categoria)
        produto.nome = nome
        produto.descricao = descricao
        preco_de_custo_in_decimal = Decimal(preco_de_custo.replace(',','.'))
        produto.preco_de_custo = preco_de_custo_in_decimal
        preco_in_decimal = Decimal(preco.replace(',','.'))
        produto.preco = preco_in_decimal
        produto.categoria = categoria_by_id
        produto.marca = marca
        produto.cor = cor
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

def alterar_imagem_principal(request, id_produto):
    imagem = request.FILES.get('imagem_principal')
    produto = Produtos.objects.get(id=id_produto)
    produto.imagem_principal = imagem
    produto.save()
    messages.add_message(request, constants.SUCCESS, 'Imagem alterada com sucesso.')
    return redirect(f'/produtos/ver_produto/{id_produto}')


def incluir_imagens(request, id_produto):
    imagens = request.FILES.getlist('imagens')
    for img in imagens:
        imagem = Imagens(produto_id=id_produto, foto=img)
        imagem.save()
    messages.add_message(request, constants.SUCCESS, 'Imagem incluída com sucesso.')
    return redirect(f'/produtos/ver_produto/{id_produto}')

def excluir_imagem(request, id_imagem, id_produto):
    imagem = Imagens.objects.get(id=id_imagem)
    imagem.delete()
    messages.add_message(request, constants.SUCCESS, 'Imagem excluída com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id_produto}')

def excluir_imagem_principal(request, id_produto):
    produto = Produtos.objects.get(id=id_produto)
    produto.imagem_principal.delete()
    messages.add_message(request, constants.SUCCESS, 'Imagem excluída com sucesso.')
    return redirect(f'/produtos/ver_produto/{id_produto}')
