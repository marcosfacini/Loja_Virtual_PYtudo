from django.shortcuts import render, redirect
from .forms import CadastroUsuario, AtualizarUsuario
from .models import Usuarios
from django.contrib import messages
from django.contrib.messages import constants 
from django.urls import reverse
from rolepermissions.checkers import has_permission
from rolepermissions.roles import assign_role
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator, has_permission_decorator
from django.core.paginator import Paginator
from datetime import datetime
from cpf_field.validators import validate_cpf
from django.core.exceptions import ValidationError



# @login required
def info_adicional_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuario(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS, 'Usuario criado com sucesso.')
            return redirect('home')
        else:
            messages.add_message(request, constants.ERROR, 'Não foi possível cadastrar o usuário.')
    else:
        form = CadastroUsuario(initial={'usuario': request.user})
    return render(request, 'info_adicional_usuario.html', {'form': form})
    
@has_permission_decorator('gerenciar_usuarios') 
def listar_usuarios(request):
    usuarios = Usuarios.objects.all()

    nome_filtrar = request.GET.get('nome')
    if nome_filtrar:
        usuarios = usuarios.filter(nome__icontains=nome_filtrar)

    email_filtrar = request.GET.get('email') 
    if email_filtrar:
        usuarios = usuarios.filter(usuario__email__icontains=email_filtrar)

    endereco_filtrar = request.GET.get('endereco')
    if endereco_filtrar:
        usuarios = usuarios.filter(endereco__icontains=endereco_filtrar)

    bairro_filtrar = request.GET.get('bairro')
    if bairro_filtrar:
        usuarios = usuarios.filter(bairro__icontains=bairro_filtrar)

    cidade_filtrar = request.GET.get('cidade')
    if cidade_filtrar:
        usuarios = usuarios.filter(cidade__icontains=cidade_filtrar)

    estado_filtrar = request.GET.get('estado')
    if estado_filtrar:
        usuarios = usuarios.filter(estado=estado_filtrar)

    celular_filtrar = request.GET.get('celular')
    if celular_filtrar:
        usuarios = usuarios.filter(celular=celular_filtrar)

    cpf_filtrar = request.GET.get('cpf')
    if cpf_filtrar:
        usuarios = usuarios.filter(cpf=cpf_filtrar)

    data_de_nascimento_filtrar = request.GET.get('data_de_nascimento')
    if data_de_nascimento_filtrar:
        data_convertida = datetime.strptime(data_de_nascimento_filtrar, "%d/%m/%Y").strftime('%Y-%m-%d')
        usuarios = usuarios.filter(data_de_nascimento=data_convertida)

    usuarios_ordenados = usuarios.order_by('-id')
    paginacao = Paginator(usuarios_ordenados, 4)
    page = request.GET.get('page')
    usuarios_paginados = paginacao.get_page(page)

    return render(request, 'listar_usuarios.html', {'usuarios_paginados': usuarios_paginados}) 

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
    usuario = Usuarios.objects.get(id=id)
    if request.method == 'POST':
        form = AtualizarUsuario(request.POST)
        try:
            nome = request.POST.get('nome')
            usuario.nome = nome
            cpf = request.POST.get('cpf')
            validate_cpf(cpf)
            usuario.cpf = cpf
            data_de_nascimento = request.POST.get('data_de_nascimento')
            data_convertida = datetime.strptime(data_de_nascimento, "%d/%m/%Y")
            usuario.data_de_nascimento = data_convertida
            celular = request.POST.get('celular')
            usuario.celular = celular
            endereco = request.POST.get('endereco')
            usuario.endereco = endereco
            numero_endereco = request.POST.get('numero_endereco')
            usuario.numero_endereco = numero_endereco
            complemento = request.POST.get('complemento')
            usuario.complemento = complemento
            bairro = request.POST.get('bairro')
            usuario.bairro = bairro
            cidade = request.POST.get('cidade')
            usuario.cidade = cidade
            estado = request.POST.get('estado')
            usuario.estado = estado
            if form.is_valid():
                usuario.save()
                messages.add_message(request, constants.SUCCESS, 'Usuario atualizado com sucesso.')
                return redirect(f'/usuarios/atualizar_usuario/{id}')
            else:
                messages.add_message(request, constants.ERROR, 'Não foi possível atualizar o formulário')
        except ValidationError as error:
            messages.add_message(request, constants.ERROR, f'{error}')
            return render(request, 'atualizar_usuario.html', {'form': form,
                                                      'usuario': usuario})
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possível atualizar o formulário')
            return render(request, 'atualizar_usuario.html', {'form': form,
                                                      'usuario': usuario})     
    else:
        dados = usuario.__dict__
        form = AtualizarUsuario(dados)
    return render(request, 'atualizar_usuario.html', {'form': form,
                                                      'usuario': usuario})







