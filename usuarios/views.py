from django.shortcuts import render, HttpResponse, redirect
from .forms import CadastroUsuario
from .models import Usuarios
from django.contrib import messages
from django.contrib.messages import constants 
from django.urls import reverse
from rolepermissions.checkers import has_permission
from rolepermissions.roles import assign_role
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator, has_permission_decorator

def info_adicional_usuario(request):
    form = CadastroUsuario()
    return render(request, 'info_adicional_usuario.html', {'form': form})

def cadastrar_usuario(request):
    cadastro = CadastroUsuario(request.POST)
    if cadastro.is_valid():
        cadastro.save()
        messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso.')
        return redirect('/produtos/listar_produtos')
    else:
        messages.add_message(request, constants.ERROR, 'Não foi possível cadastrar o usuário.')
    return redirect('/usuarios/info_adicional_usuario')

@has_permission_decorator('gerenciar_usuarios')
def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@has_permission_decorator('gerenciar_usuarios')
def excluir_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    usuario.delete()
    messages.add_message(request, constants.SUCCESS, 'Usuario excluído com sucesso.')
    return redirect('/usuarios/listar_usuarios')

def ver_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    return render(request, 'ver_usuario.html', {'usuario': usuario,})

def atualizar_usuario(request, id):
    if request.method == 'GET':    
        usuario = Usuarios.objects.get(id=id)
        return render(request, 'atualizar_usuario.html', {'usuario': usuario})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        celular = request.POST.get('celular')
        endereco = request.POST.get('endereco')
        numero_endereco = request.POST.get('numero_endereco')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        usuario = Usuarios.objects.get(id=id)
        usuario.nome = nome
        usuario.celular = celular
        usuario.endereco = endereco
        usuario.numero_endereco = numero_endereco
        usuario.bairro = bairro
        usuario.estado = estado
        usuario.save()
        messages.add_message(request, constants.SUCCESS, 'Usuario atualizado com sucesso.')
        return redirect(f'/usuarios/ver_usuario/{id}')





