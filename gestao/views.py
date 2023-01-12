from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import constants 
from rolepermissions.roles import assign_role
from rolepermissions.permissions import grant_permission, revoke_permission
from django.contrib.auth.models import User
from rolepermissions.decorators import has_role_decorator

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



