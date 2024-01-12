from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.roles import assign_role
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator
from produtos.models import Produtos, Categoria, DestacadosHome
from django.core.paginator import Paginator
from decimal import Decimal
from .models import Banner
from vendas.models import CupomDesconto
from checkout.models import Pedido
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password

@login_required
def criar_gerente(request):
    if request.user.is_superuser:
        return render(request, 'criar_gerente.html')
    else:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para executar essa função.')
        return redirect('home')

@login_required
def salvar_gerente(request):
    if request.user.is_superuser:
        email = request.POST.get('email')
        senha_provisoria = request.POST.get('senha_provisoria')
        senha_provisoria2 = request.POST.get('senha_provisoria2')

        if validar_formulario_gerente(request, email, senha_provisoria, senha_provisoria2):
            gerente = User.objects.create_user(username=email,
                                        email=email,
                                        password=senha_provisoria)
            assign_role(gerente, 'gerente')
            messages.add_message(request, constants.SUCCESS, 'Gerente cadastrado com sucesso')
            return redirect('home')
        else:
            return redirect('criar_gerente')
    else:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para executar essa função.')
        return redirect('home')

@has_role_decorator('gerente')
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

@has_role_decorator('gerente')
def detalhes_produto(request, id):
    produto = Produtos.objects.get(id=id)
    return render(request, 'detalhes_produto.html', {'produto': produto})

@has_role_decorator('gerente')
def painel_controle(request):
    return render(request, 'painel_controle.html')

@has_role_decorator('gerente')
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

@has_role_decorator('gerente')
def exibicao_home(request):
    produtos = request.POST.getlist('selecionados[]')
    acao = request.POST.get('acao')
    if produtos == []:
        messages.add_message(request, constants.ERROR, 'Selecione um produto')
        return redirect('/gestao/produtos_home')

    if acao == 'incluir':
        try:
            for produto in produtos:
                if DestacadosHome.objects.filter(produto_id=produto).exists() == False:
                    home = DestacadosHome(produto_id=produto) 
                    home.save()
            messages.add_message(request, constants.SUCCESS, 'Produtos adicionados na home com sucesso')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao adicionar produtos. Tente novamente mais tarde')

    if acao == 'excluir':
        try:
            for produto in produtos:
                home = DestacadosHome.objects.filter(produto_id=produto)
                for obj in home:
                    obj.delete()
            messages.add_message(request, constants.SUCCESS, 'Produtos deletados da home com sucesso')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao deletar produtos. Tente novamente mais tarde')

    return redirect('/gestao/produtos_home')

@has_role_decorator('gerente')
def gerenciar_banners(request):
    banners = Banner.objects.all()
    return render(request, 'gerenciar_banners.html', {'banners': banners})

@has_role_decorator('gerente')
def adicionar_banner(request):
    img = request.FILES.get('banner')
    titulo = request.POST.get('titulo')
    subtitulo = request.POST.get('subtitulo')
    if img:
        banner = Banner(imagem=img, titulo=titulo, subtitulo=subtitulo)
        banner.save()
        messages.add_message(request, constants.SUCCESS, 'Banner salvo com sucesso')
        return redirect('/gestao/gerenciar_banners')
    else:
        messages.add_message(request, constants.ERROR, 'Selecione uma imagem válida')
        return redirect('/gestao/gerenciar_banners')

@has_role_decorator('gerente')
def selecionar_banner(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.home = True
    banner.save()
    messages.add_message(request, constants.SUCCESS, 'Banner adicionado na home com sucesso.')
    return redirect('/gestao/gerenciar_banners')

@has_role_decorator('gerente')
def deletar_banner(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.delete()
    messages.add_message(request, constants.SUCCESS, 'Banner deletado com sucesso')
    return redirect('/gestao/gerenciar_banners')

@has_role_decorator('gerente')
def tirar_banner_home(request, id_banner):
    banner = Banner.objects.get(id=id_banner)
    banner.home = False
    banner.save()
    messages.add_message(request, constants.SUCCESS, 'Banner retirado com sucesso')
    return redirect('/gestao/gerenciar_banners')

@has_role_decorator('gerente')
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

@has_role_decorator('gerente')
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

@has_role_decorator('gerente')
def consultar_pedidos(request):
    pedidos = Pedido.objects.all()
    numero_filtrar = request.GET.get('numero')
    if numero_filtrar:
        pedidos = pedidos.filter(id=numero_filtrar)
    pedidos_ordenados = pedidos.order_by('-id')
    paginacao = Paginator(pedidos_ordenados, 10)
    page = request.GET.get('page')
    pedidos = paginacao.get_page(page)
    return render(request, 'consultar_pedidos.html', {'pedidos': pedidos})

def validar_formulario_gerente(request, email, senha1, senha2):
   try:
       EmailValidator()(email)
   except ValidationError as error:
        messages.add_message(request, constants.ERROR, f'{error}')
        return False

   if senha1 != senha2:
        messages.add_message(request, constants.ERROR, 'As senhas precisam ser iguais.')
        return False
   
   try:
       validate_password(senha1)
   except ValidationError as error:
        messages.add_message(request, constants.ERROR, f'{error}')
        return False

   return True

