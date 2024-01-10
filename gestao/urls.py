from django.urls import path
from . import views

urlpatterns = [
    path('criar_gerente/', views.criar_gerente, name="criar_gerente"),
    path('salvar_gerente/', views.salvar_gerente, name='salvar_gerente'),
    path('adm_estoque/', views.adm_estoque, name='adm_estoque'),
    path('detalhes_produto/<int:id>', views.detalhes_produto, name='detalhes_produto'),
    path('painel_controle/', views.painel_controle, name='painel_controle'),
    path('produtos_home/', views.produtos_home, name='produtos_home'),
    path('exibicao_home/', views.exibicao_home, name='exibicao_home'),
    path('gerenciar_banners/', views.gerenciar_banners, name='gerenciar_banners'),
    path('adicionar_banner/', views.adicionar_banner, name='adicionar_banner'),
    path('selecionar_banner/<int:id_banner>', views.selecionar_banner, name='selecionar_banner'),
    path('deletar_banner/<int:id_banner>', views.deletar_banner, name='deletar_banner'),
    path('tirar_banner_home/<int:id_banner>', views.tirar_banner_home, name='tirar_banner_home'),
    path('gerenciar_cupons/', views.gerenciar_cupons, name='gerenciar_cupons'),
    path('alterar_cupons/', views.alterar_cupons, name='alterar_cupons'),
    path('consultar_pedidos/', views.consultar_pedidos, name='consultar_pedidos'),
    
   
]

