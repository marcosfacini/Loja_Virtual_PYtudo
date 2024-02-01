from django.shortcuts import render, redirect
from .forms import CadastroUsuario, AtualizarUsuario
from .models import Usuarios, RegistroAlteracaoUsuario
from checkout.models import Pedido, ItensPedido
from django.contrib import messages
from django.contrib.messages import constants 
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator
from django.core.paginator import Paginator
from datetime import datetime
from cpf_field.validators import validate_cpf
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from rolepermissions.checkers import has_role
from pytudo.roles import Gerente



@login_required
def info_adicional_usuario(request):
    try: 
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
        messages.add_message(request, constants.SUCCESS, 'Bem vindo ao seu perfil.')
        return redirect('perfil_usuario')
    except ObjectDoesNotExist:
        if request.method == 'POST':
            form = CadastroUsuario(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Cadastro completo com sucesso.')
                return redirect('home')
            else:
                messages.add_message(request, constants.ERROR, 'Não foi possível cadastrar o usuário.')
        else:
            form = CadastroUsuario(initial={'usuario': request.user})
        return render(request, 'info_adicional_usuario.html', {'form': form})
    
@has_role_decorator('gerente') 
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

@has_role_decorator('gerente')
def excluir_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    user = User.objects.get(username=usuario.usuario)
    usuario.delete()
    user.delete()
    messages.add_message(request, constants.SUCCESS, 'Usuario excluído com sucesso.')
    return redirect('/usuarios/listar_usuarios')

@has_role_decorator('gerente')
def ver_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    registros = RegistroAlteracaoUsuario.objects.filter(usuario_id=id)
    pedidos = Pedido.objects.filter(usuario_id=usuario.id)
    return render(request, 'ver_usuario.html', {'usuario': usuario, 'registros': registros, 'pedidos': pedidos}) 

@has_role_decorator('gerente')
def atualizar_usuario(request, id):
    usuario = Usuarios.objects.get(id=id)
    if request.method == 'POST':
        form = AtualizarUsuario(request.POST)
        try:
            usuario.nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            validate_cpf(cpf)
            usuario.cpf = cpf
            data_de_nascimento = request.POST.get('data_de_nascimento')
            data_convertida = datetime.strptime(data_de_nascimento, "%d/%m/%Y")
            usuario.data_de_nascimento = data_convertida
            usuario.celular = request.POST.get('celular')
            usuario.endereco = request.POST.get('endereco')
            usuario.numero_endereco = request.POST.get('numero_endereco')
            usuario.complemento = request.POST.get('complemento')
            usuario.bairro = request.POST.get('bairro')
            usuario.cidade = request.POST.get('cidade')
            usuario.estado = request.POST.get('estado')
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

@login_required
def perfil_usuario(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para criar um perfil.')
        return redirect(f'/usuarios/info_adicional_usuario')
    return render(request, 'perfil_usuario.html', {'usuario': usuario})
     
@login_required
def usuario_atualiza_cadastro(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para criar um perfil.')
        return redirect(f'/usuarios/info_adicional_usuario')
    if request.method == 'POST':
        form = AtualizarUsuario(request.POST)
        try:
            usuario.nome = request.POST.get('nome')
            cpf = request.POST.get('cpf')
            validate_cpf(cpf)
            usuario.cpf = cpf
            data_de_nascimento = request.POST.get('data_de_nascimento')
            data_convertida = datetime.strptime(data_de_nascimento, "%d/%m/%Y")
            usuario.data_de_nascimento = data_convertida
            usuario.celular = request.POST.get('celular')
            usuario.endereco = request.POST.get('endereco')
            usuario.numero_endereco = request.POST.get('numero_endereco')
            usuario.complemento = request.POST.get('complemento')
            usuario.bairro = request.POST.get('bairro')
            usuario.cidade = request.POST.get('cidade')
            usuario.estado = request.POST.get('estado')
            if form.is_valid():
                usuario.save()
                messages.add_message(request, constants.SUCCESS, 'Usuario atualizado com sucesso.')
                return redirect(f'/usuarios/usuario_atualiza_cadastro/')
            else:
                messages.add_message(request, constants.ERROR, 'Não foi possível atualizar o formulário')
        except ValidationError as error:
            messages.add_message(request, constants.ERROR, f'{error}')
            return render(request, 'usuario_atualiza_cadastro.html', {'form': form,
                                                      'usuario': usuario})
        except:
            messages.add_message(request, constants.ERROR, 'Não foi possível atualizar o formulário')
            return render(request, 'usuario_atualiza_cadastro.html', {'form': form,
                                                      'usuario': usuario})     
    else:
        dados = usuario.__dict__
        form = AtualizarUsuario(dados)
    return render(request, 'usuario_atualiza_cadastro.html', {'form': form,
                                                      'usuario': usuario})

@login_required
def alteracoes_usuario(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para criar um perfil.')
        return redirect(f'/usuarios/info_adicional_usuario')
    registros = RegistroAlteracaoUsuario.objects.filter(usuario_id=usuario.id)
    return render(request, 'alteracoes_usuario.html', {'usuario': usuario, 'registros': registros})

@login_required
def meus_pedidos(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para criar um perfil.')
        return redirect(f'/usuarios/info_adicional_usuario')
    pedidos = Pedido.objects.filter(usuario_id=usuario.id)
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})

@login_required
def ver_pedido(request, id):
    if has_role(request.user, Gerente):
        pedido = Pedido.objects.get(id=id)
        itens = ItensPedido.objects.filter(pedido=pedido)
        return render(request, 'ver_pedido.html', {'pedido': pedido, 'itens': itens})
    else:
        try:
            usuario = Usuarios.objects.get(usuario_id=request.user.id)
        except ObjectDoesNotExist:
            messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para criar um perfil.')
            return redirect(f'/usuarios/info_adicional_usuario')
        pedido = Pedido.objects.filter(usuario=usuario).filter(id=id).first()
        itens = ItensPedido.objects.filter(pedido=pedido)
        return render(request, 'ver_pedido.html', {'pedido': pedido, 'itens': itens})




