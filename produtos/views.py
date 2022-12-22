from django.shortcuts import render, HttpResponse, redirect
from .models import Produtos, Categoria
from .forms import CadastroProduto
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.decorators import has_permission_decorator


def listar_produtos(request):
    produtos = Produtos.objects.all()
    return render(request, 'produtos.html', {'produtos': produtos})

@has_permission_decorator('cadastrar_produto')
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
    return render(request, 'ver_produto.html', {'produto': produto})

def excluir_produto(request, id):
    produto = Produtos.objects.get(id=id)
    produto.delete()
    return redirect('/produtos/listar_produtos')

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

def cadastrar_categoria(request):
    nome = request.POST.get('nome')
    categoria = Categoria(nome=nome)
    categoria.save()
    messages.add_message(request, constants.SUCCESS, 'Categoria salva com sucesso.')
    return redirect('/produtos/listar_categorias')

def excluir_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    messages.add_message(request, constants.SUCCESS, 'Categoria excluída com sucesso.')
    return redirect('/produtos/listar_categorias')

