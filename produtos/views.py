from django.shortcuts import render, redirect
from .models import Produtos, Categoria, Avaliacao, Imagens
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.decorators import has_role_decorator
from decimal import Decimal
from django.core.paginator import Paginator
from .forms import CadastrarProduto, AtualizarEspecificacao
from usuarios.models import Usuarios
import random 
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



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

    total_produtos = produtos.count()
    produtos_ordenados = produtos.order_by('-id')
    paginacao = Paginator(produtos_ordenados, 4)

    ordenacao = request.GET.get('ordenacao')
    if ordenacao == 'maior':
        produtos_ordenados = produtos.order_by('-preco')
        paginacao = Paginator(produtos_ordenados, 4)

    elif ordenacao == 'menor':
        produtos_ordenados = produtos.order_by('preco')
        paginacao = Paginator(produtos_ordenados, 4)
    
    page = request.GET.get('page')
    produtos_paginados = paginacao.get_page(page)

    return render(request, 'produtos.html', {'produtos_paginados': produtos_paginados,
                                             'total_produtos': total_produtos,
                                             'categorias': categorias})

@has_role_decorator('gerente') 
def cadastrar_produto(request):
    if request.method == 'POST':
        form = CadastrarProduto(request.POST, request.FILES)
        if form.is_valid():
            produto = Produtos(nome=request.POST.get('nome'), 
                            descricao=request.POST.get('descricao'), 
                            preco_de_custo=convercao_decimal_or_none(request.POST.get('preco_de_custo')), 
                            preco=convercao_decimal_or_none(request.POST.get('preco')), 
                            categoria_id=request.POST.get('categoria'), 
                            marca=request.POST.get('marca'), 
                            cor=request.POST.get('cor'), 
                            quantidade=request.POST.get('quantidade'),
                            imagem_principal=request.FILES.get('imagem_principal'),
                            especificacao=request.POST.get('especificacao'),
                            frete_gratis=form.cleaned_data['frete_gratis'],
                            altura=convercao_decimal_or_none(request.POST.get('altura')),
                            largura=convercao_decimal_or_none(request.POST.get('largura')),
                            profundidade=convercao_decimal_or_none(request.POST.get('profundidade')),
                            peso=convercao_decimal_or_none(request.POST.get('peso'))
                            )
            produto.save()

            imagens = request.FILES.getlist('outras_imagens')
            if imagens:
                for img in imagens:
                    imagem = Imagens(produto=produto, foto=img)
                    imagem.save()
            messages.add_message(request, constants.SUCCESS, 'Produto salvo com sucesso.')
            return redirect('/gestao/adm_estoque')
    else:
        form = CadastrarProduto()
    return render(request, 'cadastrar_produto.html', {'form': form})

def ver_produto(request, id):
    produto = Produtos.objects.get(id=id)
    avaliacoes = Avaliacao.objects.filter(produto=id)
    imagens = Imagens.objects.filter(produto_id=id)
    produtos_relacionados = Produtos.objects.filter(categoria=produto.categoria).exclude(id=produto.id)
    produtos_relacionados = random.sample(list(produtos_relacionados), min(4, len(produtos_relacionados)))
    if avaliacoes:
        estrelas = []
        for av in avaliacoes:
            estrelas.append(int(av.estrelas))
        media_estrelas = str(round(sum(estrelas) / avaliacoes.count()))
    else:
        media_estrelas = str(5)
    avaliacoes_ordenadas = avaliacoes.order_by('-data_avaliacao')
    return render(request, 'ver_produto.html', {'produto': produto,
                                                'avaliacoes_ordenadas': avaliacoes_ordenadas,
                                                'imagens': imagens,
                                                'media_estrelas': media_estrelas,
                                                'produtos_relacionados': produtos_relacionados})

@has_role_decorator('gerente')
def excluir_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    messages.add_message(request, constants.SUCCESS, 'Produto excluído com sucesso.')
    return redirect('/gestao/adm_estoque')

@has_role_decorator('gerente') 
def listar_categorias(request):
    categorias = Categoria.objects.all()
    nome_filtrar = request.GET.get('nome')
    if nome_filtrar:
        categorias = categorias.filter(nome__icontains=nome_filtrar)
    categorias_ordenadas = categorias.order_by('nome')
    paginacao = Paginator(categorias_ordenadas, 5)
    page = request.GET.get('page')
    categorias = paginacao.get_page(page)
    return render(request, 'listar_categorias.html', {'categorias': categorias})

@has_role_decorator('gerente')
def cadastrar_categoria(request):
    nome = request.POST.get('nome')
    categoria = Categoria(nome=nome)
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria salva com sucesso.')
    return redirect('/produtos/listar_categorias')

@has_role_decorator('gerente')
def excluir_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    messages.add_message(request, constants.SUCCESS, 'Categoria excluída com sucesso.')
    return redirect('/produtos/listar_categorias')

@has_role_decorator('gerente')
def alterar_produto(request, id):
    if request.method == 'GET':
        produto = Produtos.objects.get(id=id)
        categorias = Categoria.objects.all()
        imagens = Imagens.objects.filter(produto_id=id)
        form_especificacao = AtualizarEspecificacao()
        return render(request, 'alterar_produto.html', {'produto': produto,
                                                        'categorias': categorias,
                                                        'imagens': imagens,
                                                        'form_especificacao': form_especificacao})
    elif request.method == 'POST':
        produto = Produtos.objects.get(id=id)
        produto.nome = request.POST.get('nome')
        produto.descricao = request.POST.get('descricao')
        produto.preco_de_custo = convercao_decimal_or_none(request.POST.get('preco_de_custo'))
        produto.preco = convercao_decimal_or_none(request.POST.get('preco'))

        categoria = request.POST.get('categoria')
        if categoria == '':
            categoria = None
            produto.categoria = categoria
        else:
            categoria_by_id = Categoria.objects.get(id=categoria)
            produto.categoria = categoria_by_id
        
        produto.marca = request.POST.get('marca')
        produto.cor = request.POST.get('cor')
        produto.quantidade = request.POST.get('quantidade')
        if request.POST.get('frete_gratis') == 'sim':
            frete_gratis = True
        else:
            frete_gratis = False
        produto.frete_gratis = frete_gratis
        produto.altura = convercao_decimal_or_none(request.POST.get('altura'))
        produto.largura = convercao_decimal_or_none(request.POST.get('largura'))
        produto.profundidade = convercao_decimal_or_none(request.POST.get('profundidade'))
        produto.peso = convercao_decimal_or_none(request.POST.get('peso'))
        
        produto.save()
        messages.add_message(request, constants.SUCCESS, 'Produto atualizado com sucesso.')
        return redirect(f'/produtos/alterar_produto/{id}')

@login_required
def salvar_avaliacao(request, id_produto):
    try:
        usuario = Usuarios.objects.get(usuario=request.user)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro para poder comentar.')
        return redirect('/usuarios/info_adicional_usuario')
    estrelas = request.POST.get('estrelas')
    comentario = request.POST.get('comentario')
    if estrelas == None:
        messages.add_message(request, constants.ERROR, 'Por favor escolha a quantidade de estrelas.')
        return redirect(f'/produtos/ver_produto/{id_produto}')
    avalicao = Avaliacao(usuario=usuario, produto_id=id_produto, estrelas=estrelas, comentario=comentario)
    avalicao.save()
    return redirect(f'/produtos/ver_produto/{id_produto}')

@has_role_decorator('gerente')
def excluir_avaliacao(request, id_avaliacao, id_produto):
    avaliacao = Avaliacao.objects.get(id=id_avaliacao)
    avaliacao.delete()
    return redirect(f'/produtos/ver_produto/{id_produto}')

@has_role_decorator('gerente')
def alterar_imagem_principal(request, id_produto):
    imagem = request.FILES.get('imagem_principal')
    produto = Produtos.objects.get(id=id_produto)
    produto.imagem_principal = imagem
    produto.save()
    messages.add_message(request, constants.SUCCESS, 'Imagem alterada com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id_produto}')

@has_role_decorator('gerente')
def incluir_imagens(request, id_produto):
    imagens = request.FILES.getlist('imagens')
    for img in imagens:
        imagem = Imagens(produto_id=id_produto, foto=img)
        imagem.save()
    messages.add_message(request, constants.SUCCESS, 'Imagem incluída com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id_produto}')

@has_role_decorator('gerente')
def excluir_imagem(request, id_imagem, id_produto):
    imagem = Imagens.objects.get(id=id_imagem)
    imagem.delete()
    messages.add_message(request, constants.SUCCESS, 'Imagem excluída com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id_produto}')

@has_role_decorator('gerente')
def excluir_imagem_principal(request, id_produto):
    produto = Produtos.objects.get(id=id_produto)
    produto.imagem_principal.delete()
    messages.add_message(request, constants.SUCCESS, 'Imagem excluída com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id_produto}')

@has_role_decorator('gerente')
def atualizar_especificacao(request, id):
    produto = Produtos.objects.get(id=id)
    especificacao = request.POST.get('especificacao')
    produto.especificacao = especificacao
    produto.save()
    messages.add_message(request, constants.SUCCESS, 'Especificação atualizada com sucesso.')
    return redirect(f'/produtos/alterar_produto/{id}')

def convercao_decimal_or_none(campo_do_form):
    if campo_do_form == '':
        campo_do_form = None
    else:
        campo_do_form = Decimal(campo_do_form.replace(',','.'))
    return campo_do_form

def calcular_frete_produto(request, id_produto):
    cep = validar_cep(request.POST.get('cep'))
    if cep:
        produto = Produtos.objects.get(id=id_produto)
        return redirect(f'/produtos/ver_produto/{id_produto}')
    else:
        messages.add_message(request, constants.ERROR, 'CPF INVÁLIDO.')
        return redirect(f'/produtos/ver_produto/{id_produto}')

def validar_cep(cep):
    cep = cep.replace('-', '')
    if cep.isdigit() and len(cep) == 8:
        return cep
    else:
        return None

def teste(request):
    categorias = Categoria.objects.all()
    chave_publica = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr+ZqgD892U9/HXsa7XqBZUayPquAfh9xx4iwUbTSUAvTlmiXFQNTp0Bvt/5vK2FhMj39qSv1zi2OuBjvW38q1E374nzx6NNBL5JosV0+SDINTlCG0cmigHuBOyWzYmjgca+mtQu4WczCaApNaSuVqgb8u7Bd9GCOL4YJotvV5+81frlSwQXralhwRzGhj/A57CGPgGKiuPT+AOGmykIGEZsSD9RKkyoKIoc0OS8CPIzdBOtTQCIwrLn2FxI83Clcg55W8gkFSOS6rWNbG5qFZWMll6yl02HtunalHmUlRUL66YeGXdMDC2PuRcmZbGO5a/2tbVppW6mfSWG3NPRpgwIDAQAB'
    return render(request, 'teste.html', {'categorias': categorias, 'chave_publica': chave_publica})