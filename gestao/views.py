from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.roles import assign_role
from rolepermissions.permissions import grant_permission, revoke_permission
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator
from produtos.models import Produtos, Categoria
from django.core.paginator import Paginator
from decimal import Decimal

@has_role_decorator('gestor')
def criar_gerente(request):
    return render(request, 'criar_gerente.html')

@has_role_decorator('gestor')
def salvar_gerente(request):
    email = request.POST.get('email')
    senha_provisoria = request.POST.get('senha_provisoria')
    gerente = User.objects.create_user(username=email,
                                 email=email,
                                 password=senha_provisoria)
    assign_role(gerente, 'gerente')
    messages.add_message(request, constants.SUCCESS, 'Gerente cadastrado com sucesso')
    return redirect('/gestao/criar_gerente')

@has_role_decorator('gestor')
def criar_gestor(request):
    return render(request, 'criar_gestor.html')

@has_role_decorator('gestor')
def salvar_gestor(request):
    email = request.POST.get('email')
    senha_provisoria = request.POST.get('senha_provisoria')
    gestor = User.objects.create_user(username=email,
                                 email=email,
                                 password=senha_provisoria)
    assign_role(gestor, 'gestor')
    messages.add_message(request, constants.SUCCESS, 'Gestor cadastrado com sucesso')
    return redirect('/produtos/listar_produtos')

def adm_estoque(request):
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

    preco_de_custo_menor_filtrar = request.GET.get('preco_de_custo_menor_filtrar')
    if preco_de_custo_menor_filtrar:
        preco_de_custo_menor_filtrar_decimal = Decimal(preco_de_custo_menor_filtrar.replace(',','.'))
        produtos = produtos.filter(preco_de_custo__lt=preco_de_custo_menor_filtrar_decimal)
    
    preco_de_custo_maior_filtrar = request.GET.get('preco_de_custo_maior_filtrar')
    if preco_de_custo_maior_filtrar:
        preco_de_custo_maior_filtrar_decimal = Decimal(preco_de_custo_maior_filtrar.replace(',','.'))
        produtos = produtos.filter(preco_de_custo__gt=preco_de_custo_maior_filtrar_decimal)

    marca_filtar = request.GET.get('marca')
    if marca_filtar:
        produtos = produtos.filter(marca__icontains=marca_filtar)

    cor_filtar = request.GET.get('cor')
    if cor_filtar:
        produtos = produtos.filter(cor__icontains=cor_filtar)

    quantidade_menor_filtrar = request.GET.get('quantidade_menor_filtrar')
    if quantidade_menor_filtrar:
        produtos = produtos.filter(quantidade__lt=quantidade_menor_filtrar)

    quantidade_maior_filtrar = request.GET.get('quantidade_maior_filtrar')
    if quantidade_maior_filtrar:
        produtos = produtos.filter(quantidade__gt=quantidade_maior_filtrar)


    produtos_ordenados = produtos.order_by('-id')
    paginacao = Paginator(produtos_ordenados, 8)
    page = request.GET.get('page')
    produtos_paginados = paginacao.get_page(page)

    return render(request, 'adm_estoque.html', {'produtos_paginados': produtos_paginados,
                                                'categorias': categorias})

@has_role_decorator('gestor')
def detalhes_produto(request, id):
    produto = Produtos.objects.get(id=id)
    return render(request, 'detalhes_produto.html', {'produto': produto})



