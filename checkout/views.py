from django.shortcuts import render, redirect
import json, requests
from django.contrib import messages
from django.contrib.messages import constants
from usuarios.models import Usuarios
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from produtos.models import Produtos
from vendas.models import CupomDesconto
from .models import Pedido, ItensPedido
from decimal import Decimal
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response


@login_required
def checkout(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para comprar.')
        return redirect(f'/usuarios/info_adicional_usuario')
    #chave_publica = {}
    #chave_publica['publicKey'] = get_chave_publica()
    if verificar_estoque(request) == False:
        return redirect(f'/vendas/carrinho')
    chave_publica = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr+ZqgD892U9/HXsa7XqBZUayPquAfh9xx4iwUbTSUAvTlmiXFQNTp0Bvt/5vK2FhMj39qSv1zi2OuBjvW38q1E374nzx6NNBL5JosV0+SDINTlCG0cmigHuBOyWzYmjgca+mtQu4WczCaApNaSuVqgb8u7Bd9GCOL4YJotvV5+81frlSwQXralhwRzGhj/A57CGPgGKiuPT+AOGmykIGEZsSD9RKkyoKIoc0OS8CPIzdBOtTQCIwrLn2FxI83Clcg55W8gkFSOS6rWNbG5qFZWMll6yl02HtunalHmUlRUL66YeGXdMDC2PuRcmZbGO5a/2tbVppW6mfSWG3NPRpgwIDAQAB'
    return render(request, 'checkout.html', {'chave_publica': chave_publica})

# preciso criar a chave publica apenas uma vez e depois criar uma nova funcao apenas para consultar a minha chave publica?
def get_chave_publica():
    url = 'https://sandbox.api.pagseguro.com/public-keys/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'E27D533A220041F689D7C53BE6A84D74'
    }
    body = json.dumps({
        "type": "card"
    })
    reqs = requests.post(url,headers=headers,data=body)
    return reqs.json()['public_key']

@login_required
def processar_metodo_pagamento(request):
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para comprar.')
        return redirect(f'/usuarios/info_adicional_usuario')
    metodo_de_pagamento = request.POST['paymentMethod']
    if metodo_de_pagamento == 'creditCard':
        return pagamento_credito(request)
    elif metodo_de_pagamento == 'boleto':
        return pagamento_boleto(request)
    elif metodo_de_pagamento == 'pix':
        return pagamento_pix(request)
    else:
        messages.add_message(request, constants.ERROR, 'Erro ao processar o pagamento. Por favor tente novamente mais tarde')
        return redirect(f'/checkout/checkout')

def pagamento_credito(request):
    if not request.user.is_authenticated:
        messages.add_message(request, constants.ERROR, 'E preciso estar logado a uma conta para finalizar a compra.')
        return redirect(f'/accounts/login')
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para finalizar a compra.')
        return redirect(f'/usuarios/info_adicional_usuario')
    
    if verificar_estoque(request) == False:
        return redirect(f'/vendas/carrinho')
    pedido = criar_pedido(request, usuario.id)
    itens_pedidos(request, pedido)
    
    cel = usuario.celular.as_e164

    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'E27D533A220041F689D7C53BE6A84D74'
    }
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": usuario.nome,
            "email": usuario.usuario.email,
            "tax_id": usuario.cpf.replace('.', '').replace('-', ''),
            "phones": [
                {
                    "country": "55",
                    "area": cel[3] + cel[4],
                    "number": cel[-9:],
                    "type": "MOBILE"
                }
            ]
        },
        "items": itens_carrinho(request),

        "shipping": {
            "address": {
                "street": "Avenida Brigadeiro Faria Lima",
                "number": "1384",
                "complement": "apto 12",
                "locality": "Pinheiros",
                "city": "São Paulo",
                "region_code": "SP",
                "country": "BRA",
                "postal_code": "01452002"
            }
        },
        "notification_urls": [
            "https://meusite.com/notificacoes"
        ],
        "charges": [
            {
                "reference_id": str(pedido.id),
                "description": f'Cobrança referente ao pedido: {str(pedido.id)}',
                "amount": {
                    "value": total_carrinho(request),
                    "currency": "BRL"
                },
                "payment_method": {
                    'soft_descriptor':'PytudoPagBank',
                    "type": "CREDIT_CARD",
                    "installments": 1,
                    "capture": True,
                    "card": {
                        "encrypted": request.POST['encriptedCard'],
                        "security_code": request.POST['cardCvv'],
                        "holder": {
                            "name": request.POST['cardHolder']
                        },
                        "store": True
                    }
                }
            }
        ]
    })
    
    reqs = requests.post(url,headers=headers,data=body)
    erro, string_do_erro = validar_erro_pedido(reqs, pedido.id)
    if erro:
        messages.add_message(request, constants.ERROR, string_do_erro)
        return redirect(f'/checkout/checkout')
    pedido.status = reqs.json()['charges'][0]['status']
    pedido.save()
    deletar_session(request)
    return redirect(f'/usuarios/ver_pedido/{pedido.id}')

def pagamento_boleto(request):
    if not request.user.is_authenticated:
        messages.add_message(request, constants.ERROR, 'E preciso estar logado a uma conta para finalizar a compra.')
        return redirect(f'/accounts/login')
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para finalizar a compra.')
        return redirect(f'/usuarios/info_adicional_usuario')
    
    if verificar_estoque(request) == False:
        return redirect(f'/vendas/carrinho')
    pedido = criar_pedido(request, usuario.id)
    itens_pedidos(request, pedido)
    
    cel = usuario.celular.as_e164
    
    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'E27D533A220041F689D7C53BE6A84D74'
    }
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
            "name": usuario.nome,
            "email": usuario.usuario.email,
            "tax_id": usuario.cpf.replace('.', '').replace('-', ''),
            "phones": [
                {
                    "country": "55",
                    "area": cel[3] + cel[4],
                    "number": cel[-9:],
                    "type": "MOBILE"
                }
            ]
            },
            "items": itens_carrinho(request),

            "shipping": {
                "address": {
                    "street": "Avenida Brigadeiro Faria Lima",
                    "number": "1384",
                    "complement": "apto 12",
                    "locality": "Pinheiros",
                    "city": "São Paulo",
                    "region_code": "SP",
                    "country": "BRA",
                    "postal_code": "01452002"
                }
            },
            "notification_urls": [
                "https://meusite.com/notificacoes"
            ],
            "charges": [
                {
                    "reference_id": str(pedido.id),
                    "description": f'Boleto gerado referente ao pedido: {str(pedido.id)}',
                    "amount": {
                        "value": total_carrinho(request),
                        "currency": "BRL"
                    },
          "payment_method": {
            "type": "BOLETO",
            "boleto": {
              "due_date": data_vencimento(7),
              "instruction_lines": {
                "line_1": f'Boleto gerado referente ao pedido Nº: {str(pedido.id)}',
                "line_2": "Via PagSeguro"
              },
              "holder": {
                "name": usuario.nome,
                "tax_id": usuario.cpf.replace('.', '').replace('-', ''),
                "email": usuario.usuario.email,
                "address": {
                  "country": "Brasil",
                  "region": "São Paulo",
                  "region_code":"SP",
                  "city": "Sao Paulo",
                  "postal_code": "01452002",
                  "street": "Avenida Brigadeiro Faria Lima",
                  "number": "1384",
                  "locality": "Pinheiros"
                }
              }
            }
          }
        }
    ]
    })

    reqs = requests.post(url,headers=headers,data=body)
    erro, string_do_erro = validar_erro_pedido(reqs, pedido.id)
    if erro:
        messages.add_message(request, constants.ERROR, string_do_erro)
        return redirect(f'/checkout/checkout')
    pedido.link_pagamento = reqs.json()["charges"][0]['links'][0]['href']
    pedido.save()
    deletar_session(request)
    return redirect(f'/usuarios/ver_pedido/{pedido.id}')

def pagamento_pix(request):
    if not request.user.is_authenticated:
        messages.add_message(request, constants.ERROR, 'E preciso estar logado a uma conta para finalizar a compra.')
        return redirect(f'/accounts/login')
    try:
        usuario = Usuarios.objects.get(usuario_id=request.user.id)
    except ObjectDoesNotExist:
        messages.add_message(request, constants.ERROR, 'Complete o cadastro primeiro para finalizar a compra.')
        return redirect(f'/usuarios/info_adicional_usuario')
    
    if verificar_estoque(request) == False:
        return redirect(f'/vendas/carrinho')
    pedido = criar_pedido(request, usuario.id)
    itens_pedidos(request, pedido)

    cel = usuario.celular.as_e164
    
    url = 'https://sandbox.api.pagseguro.com/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization' : 'E27D533A220041F689D7C53BE6A84D74'
    }
    body = json.dumps({
        "reference_id": str(pedido.id),
        "customer": {
          "name": usuario.nome,
          "email": usuario.usuario.email,
          "tax_id": usuario.cpf.replace('.', '').replace('-', ''),
          "phones": [
              {
                  "country": "55",
                  "area": cel[3] + cel[4],
                  "number": cel[-9:],
                  "type": "MOBILE"
              }
          ]
        },
        "items": itens_carrinho(request),

        "qr_codes": [
          {
              "amount": {
                  "value": total_carrinho(request)
              },
              
          }
        ],
        "shipping": {
          "address": {
              "street": "Avenida Brigadeiro Faria Lima",
              "number": "1384",
              "complement": "apto 12",
              "locality": "Pinheiros",
              "city": "São Paulo",
              "region_code": "SP",
              "country": "BRA",
              "postal_code": "01452002"
          }
        },
        "notification_urls": [
          "https://meusite.com/notificacoes"
        ]
    })

    reqs = requests.post(url,headers=headers,data=body)
    erro, string_do_erro = validar_erro_pedido(reqs, pedido.id)
    if erro:
        messages.add_message(request, constants.ERROR, string_do_erro)
        return redirect(f'/checkout/checkout')
    pedido.link_pagamento = reqs.json()['qr_codes'][0]['links'][0]['href']
    pedido.save()
    deletar_session(request)
    return redirect(f'/usuarios/ver_pedido/{pedido.id}')

def itens_carrinho(request):
    if 'carrinho' in request.session:
        carrinho_session = request.session['carrinho']
        carrinho_ids = list(carrinho_session.keys())
        carrinho = Produtos.objects.filter(id__in=carrinho_ids)
        
        itens = []
        if request.POST['paymentMethod'] == 'pix':
            for produto in carrinho:
                item = {
                    "name": produto.nome,
                    "quantity": carrinho_session[str(produto.id)],
                    "unit_amount": int(float(produto.preco) * 100)
                }
                itens.append(item)
        else:
            for produto in carrinho:
                item = {
                    "reference_id": str(produto.id),
                    "name": produto.nome,
                    "quantity": carrinho_session[str(produto.id)],
                    "unit_amount": int(float(produto.preco) * 100)
                }
                itens.append(item)

    else:
        messages.add_message(request, constants.ERROR, 'E preciso adicionar itens ao carrinho primeiro.')
        return redirect(f'/vendas/carrinho')
    return itens

def total_carrinho(request):
    if 'total_com_desconto' in request.session:
        total = int((request.session['total_com_desconto'] * 100))
    else:
        total = int((request.session['total'] * 100))
    return total

def criar_pedido(request, id_usuario):
    metodo_de_pagamento = request.POST['paymentMethod']
    if 'total_com_desconto' in request.session:
        valor_total = Decimal(request.session['total_com_desconto'])
    else:
        valor_total = Decimal(request.session['total'])
    pedido = Pedido(usuario_id=id_usuario, valor_total=valor_total, metodo_de_pagamento=metodo_de_pagamento)
    pedido.save()
    return pedido

def itens_pedidos(request, pedido):
    produtos_ids = list(request.session['carrinho'].keys())
    quantidades = list(request.session['carrinho'].values())
    for produto_id, quantidade in zip(produtos_ids, quantidades):
        ItensPedido.objects.create(pedido=pedido, produto_id=int(produto_id), quantidade=quantidade)
    return pedido

def data_vencimento(dias):
    data_atual = datetime.now()
    data_vencimento = data_atual + timedelta(days=dias)
    data_vencimento_formatada = data_vencimento.strftime("%Y-%m-%d")
    return data_vencimento_formatada
    
def validar_erro_pedido(response_do_pedido, id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    string_do_erro = ''
    try:
        response_do_pedido.raise_for_status()
    except:
        pedido.status = 'DECLINED'
        pedido.save()
        if response_do_pedido.json()["error_messages"]:
            pedido.mensagem_de_erro = str(response_do_pedido.json()["error_messages"])
            pedido.save()
            string_do_erro = f'Erro ao realizar a cobrança: {str(response_do_pedido.json()["error_messages"][0]["description"])}. Por favor revise os dados e tente novamente.'
        else:
            pedido.mensagem_de_erro = 'Erro ao realizar o pedido. Por favor revise os dados e tente novamente.'
            pedido.save()
            string_do_erro = 'Erro ao realizar o pedido. Por favor revise os dados e tente novamente.'
        return True, string_do_erro
    return False, string_do_erro

def deletar_session(request):
    del request.session['carrinho']
    request.session.modified = True
    if 'cupom' in request.session:
        cupom = request.session['cupom']
        id_cupom = int(cupom['desconto'][2])
        cupom = CupomDesconto.objects.get(id=id_cupom)
        cupom.quantidade = cupom.quantidade - 1
        cupom.save()
        del request.session['cupom']
        request.session.modified = True
    return True

@api_view(['POST'])
def notificacao_pagseguro(request):
    try:
        alteracao_de_status = request.data['charges'][0]['status']
        id_pedido = request.data['charges'][0]['reference_id']
        pedido = Pedido.objects.get(id=id_pedido)
        pedido.status = alteracao_de_status
        pedido.save()
        return Response({'message': 'Mensagem recebida e status atualizado.'})
    except: 
        return Response({'message': 'Erro.'})
    
def verificar_estoque(request):
    produtos_ids = list(request.session['carrinho'].keys())
    quantidades_pedidas = list(request.session['carrinho'].values())
    produtos = Produtos.objects.filter(id__in=produtos_ids)
    for produto, quantidade_pedida in zip(produtos, quantidades_pedidas):
        if produto.quantidade < quantidade_pedida:
            messages.add_message(request, constants.ERROR, f'Você pediu {quantidade_pedida} unidades. Atualmene o produto {produto.nome} tem somente {produto.quantidade} em estoque. Desculpe o incoveniente.')
            return False
    return True

def subtrair_produto_estoque(request, id):
    produto = Produtos.objects.get(id=id)
    unidades_vendidas = int(request.POST.get('quantidade'))
    produto.quantidade  = produto.quantidade - unidades_vendidas
    produto.save()
    return produto.quantidade