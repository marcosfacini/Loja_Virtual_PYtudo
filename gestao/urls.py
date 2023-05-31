from django.urls import path
from . import views

urlpatterns = [
    path('criar_gerente/', views.criar_gerente, name="criar_gerente"),
    path('salvar_gerente/', views.salvar_gerente, name='salvar_gerente'),
    path('criar_gestor/', views.criar_gestor, name="criar_gestor"),
    path('salvar_gestor/', views.salvar_gestor, name='salvar_gestor'),
    path('adm_estoque/', views.adm_estoque, name='adm_estoque'),
    path('detalhes_produto/<int:id>', views.detalhes_produto, name='detalhes_produto'),
   
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

Testes automatizados

Metodo de pagamento

Calculo de frete api
inserir campo cep na model do usuario?

Tratamento de erros try/except

Soma dos produtos no carrinho

Processo de venda

verificar mensagens de erro e de sucesso nas funcões

formatar imagens antes de salvar
on cascade nao deleta imagens
tratamento de erro validacao no forms - usar form model?

usuarios anonimos podem comentar?
model avaliacao vai ter usuario on cascade?
funcao atualizar e excluir comentario

gestor seleciona quais produtos ficarao na home
Produtos em destaque/promoção num banner

Segurança/repassar permissões em todas as views visando possiveis ataques 

Pagina de perfil e botão atualizar só o usuario do perfil tem acesso  
If com request.user na view?
If dentro do template html?

Gestao desabilita/habilita contas de  usuarios e gerentes

Desabilitar urls do accounts que não vou usar

# form nao apaga a pesquisa quando a pagina e recarregada, mas mantem os pametros ate que sejam excluidos no botao limpar pesquisa

USUARIO DEVERIA PODER MUDAR O SEU CPF E SUA DATA DE NASCIMENTO DEPOIS DO CADASTRO FEITO? 
se for possivel tem que validar os campos atualizados e colocar as mascaras no cadastrar e no atualizar usuario

campo numero de endereço no cadastro de usuario e obrigatorio?

campo estado com um select com todos os estados brasileiros? teria que mudar a model e todos os forms

compensa fazer um filtro de data que busque somente pelo ano ou somente pelo mes?

PERMITIR USUARIO MUDAR EMAIL? 
ENVIO DE VALIDAÇÃO DE CASDTRO SERÁ VIA EMAL


Front:
Templates do accounts/404
Form de avaliação em estrelas
Navbar/menu
Css das paginas 
footer 
paginação estilizada
modal em botoes excluir
posicao da mensagem de erro nos forms
mascaras para campo de precos ao cadastrar - mudar o widget para aceitar a mascara?

precisa importar essa versao do bootstrap?
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
menu da nav so funciona na versao 4

tentar importar arquivos estaticos jquery pelo static

deploy/servidor e integracao com bd
containers - docker/kubernets
emails """