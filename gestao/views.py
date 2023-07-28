from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.roles import assign_role
from rolepermissions.permissions import grant_permission, revoke_permission
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator
from produtos.models import Produtos, Categoria, DestacadosHome
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Banner
from vendas.models import CupomDesconto

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
    return redirect('home')

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

def painel_controle(request):
    return render(request, 'painel_controle.html')

def produtos_home(request):
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
    paginacao = Paginator(produtos_ordenados, 10)
    page = request.GET.get('page')
    produtos_paginados = paginacao.get_page(page)
    return render(request, 'produtos_home.html', {'produtos_paginados': produtos_paginados,
                                                  'categorias': categorias}) 

def exibicao_home(request):
    produtos = request.POST.getlist('selecionados[]')
    acao = request.POST.get('acao')
    if produtos == []:
        messages.add_message(request, constants.ERROR, 'Selecione um produto')
        return redirect('/gestao/produtos_home')

    if acao == 'incluir':
        for produto in produtos:
            home = DestacadosHome(produto_id=produto)
            home.save()
        messages.add_message(request, constants.SUCCESS, 'Produtos adicionados na home com sucesso')

    if acao == 'excluir':
        for produto in produtos:
            home = DestacadosHome.objects.filter(produto_id=produto)
            for obj in home:
                obj.delete()
        messages.add_message(request, constants.SUCCESS, 'Produtos deletados da home com sucesso')

    return redirect('/gestao/produtos_home')

def gerenciar_banners(request):
    banners = Banner.objects.all()
    return render(request, 'gerenciar_banners.html', {'banners': banners})

def adicionar_banner(request):
    img = request.FILES.get('banner')
    if img:
        banner = Banner(imagem=img)
        banner.save()
        messages.add_message(request, constants.SUCCESS, 'Banner salvo com sucesso')
        return redirect('/gestao/gerenciar_banners')
    else:
        messages.add_message(request, constants.ERROR, 'Selecione uma imagem válida')
        return redirect('/gestao/gerenciar_banners')


def selecionar_banner(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.home = True
    banner.save()
    messages.add_message(request, constants.SUCCESS, 'Banner adicionado na home com sucesso.')
    return redirect('/gestao/gerenciar_banners')


def deletar_banner(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.delete()
    messages.add_message(request, constants.SUCCESS, 'Banner deletado com sucesso')
    return redirect('/gestao/gerenciar_banners')

def tirar_banner_home(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.home = False
    banner.save()
    messages.add_message(request, constants.SUCCESS, 'Banner retirado com sucesso')
    return redirect('/gestao/gerenciar_banners')

def gerenciar_cupons(request):
    cupons = CupomDesconto.objects.all()
    codigo_filtrar = request.GET.get('nome')
    if codigo_filtrar:
        cupons = cupons.filter(codigo__icontains=codigo_filtrar)

    cupons_ordenados = cupons.order_by('-id')
    paginacao = Paginator(cupons_ordenados, 10)
    page = request.GET.get('page')
    cupons_paginados = paginacao.get_page(page)
    return render(request, 'gerenciar_cupons.html', {'cupons_paginados': cupons_paginados,}) 

def alterar_cupons(request):
    cupons = request.POST.getlist('selecionados[]')
    acao = request.POST.get('acao')
    if cupons == []:
        messages.add_message(request, constants.ERROR, 'Selecione um cupom')
        return redirect('/gestao/gerenciar_cupons')
    
    if acao == 'ativar':
        for cupom in cupons:
            cumpom_selecionado = CupomDesconto.objects.get(id=cupom)
            cumpom_selecionado.ativo = True
            cumpom_selecionado.save()
        messages.add_message(request, constants.SUCCESS, 'Cupons ativados com sucesso com sucesso')


    if acao == 'desabilitar':
        for cupom in cupons:
            cumpom_selecionado = CupomDesconto.objects.get(id=cupom)
            cumpom_selecionado.ativo = False
            cumpom_selecionado.save()
        messages.add_message(request, constants.SUCCESS, 'Cupons desabilitados com sucesso com sucesso')

    if acao == 'excluir':
        for cupom in cupons:
            cumpom_selecionado = CupomDesconto.objects.get(id=cupom)
            cumpom_selecionado.delete()
        messages.add_message(request, constants.SUCCESS, 'Cupons deletados com sucesso')

    return redirect('/gestao/gerenciar_cupons')





