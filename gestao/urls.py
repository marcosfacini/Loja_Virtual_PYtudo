from django.urls import path
from . import views

urlpatterns = [
    path('criar_gerente/', views.criar_gerente, name="criar_gerente"),
    path('salvar_gerente/', views.salvar_gerente, name='salvar_gerente'),
    path('criar_gestor/', views.criar_gestor, name="criar_gestor"),
    path('salvar_gestor/', views.salvar_gestor, name='salvar_gestor'),
    path('adm_estoque/', views.adm_estoque, name='adm_estoque'),
   
]

# admin:
# marcola@gmail.com 
# marcola

# gestor:
# gestor@gmail.com
# mr.m1880

# TODO 

""" Lista de desejos - igual model carrinho? - mudar model carrinho para armazenar dados numa session?

Capturar registro do que foi atualizado usuario/produtos

Historico de compras do usuario e de vendas do produto

Controle de estoque do gerente quant/sub/add
quantidade inicial/atual
preco de custo/preco pro consumirdor/lucro
relatorio de balanço de lucro

ordenacao por tabela na lista de produtos e de usuarios do gestor

Cupom de desconto 

Validação dos campos - regex?
mensagem de erro
mascaras no forms

Testes automatizados

Metodo de pagamento

Calculo de frete api

Tratamento de erros try/except

Soma dos produtos no carrinho

Processo de venda

Mais de uma imagem por produto 

Usuario seleciona quais produtos ficarao na home

Produtos em destaque/promoção num banner

Segurança/repassar permissões em todas as views visando possiveis ataques 

Pagina de perfil e botão atualizar só o usuario do perfil tem acesso  
If com request.user na view?
If dentro do template html?

Gestao desabilita/habilita contas de  usuarios e gerentes

Desabilitar urls do accounts que não vou usar

# form nao apaga a pesquisa quando a pagina e recarregada, mas mantem os pametros ate que sejam excluidos no botao limpar pesquisa


Front:
Templates do accounts/404
Form de avaliação em estrelas
Navbar/menu
Css das paginas 
footer 
modal em botoes excluir
filtrar forma como usuario ve o celular (sem o +55)

precisa importar essa versao do bootstrap?
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
menu da nav so funciona na versao 4

tentar importar arquivos estaticos jquery pelo static

deploy/servidor e integracao com bd
emails """