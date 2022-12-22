from django.shortcuts import render, HttpResponse, redirect
from .forms import CadastroUsuario
from .models import Usuarios
from django.contrib import messages
from django.contrib.messages import constants 
from django.urls import reverse
from rolepermissions.checkers import has_permission
from rolepermissions.roles import assign_role
from rolepermissions.permissions import grant_permission, revoke_permission
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator

def login(request):
    form = CadastroUsuario()
    return render(request, 'login.html', {'form': form})

def cadastrar_usuario(request):
    cadastro = CadastroUsuario(request.POST)
    if cadastro.is_valid():
        cadastro.save()
        messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso.')
        return redirect('/produtos/listar_produtos')
    else:
        messages.add_message(request, constants.ERROR, 'Não foi possível cadastrar o usuário.')
    return redirect('/usuarios/login')

@has_role_decorator('gerente')
def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

def excluir_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    usuario.delete()
    messages.add_message(request, constants.SUCCESS, 'Usuario excluído com sucesso.')
    return redirect('/usuarios/listar_usuarios')

def ver_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    return render(request, 'ver_usuario.html', {'usuario': usuario})

def conceder_permissao(request):
    user = User.objects.get(id=4)
    # assign_role(user, 'gerente')
    # revoke_permission(user, 'cadastrar_produto')
    grant_permission(user, 'atualizar_cadastro')
    print (has_permission(user, 'atualizar_cadastro'))
    return redirect(reverse('login'))





