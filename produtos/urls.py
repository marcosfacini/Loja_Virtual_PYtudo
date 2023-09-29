from django.urls import path
from . import views

urlpatterns = [
    path('listar_produtos/', views.listar_produtos, name="listar_produtos"),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('ver_produto/<int:id>', views.ver_produto, name='ver_produto'),
    path('excluir_produto/<int:id>', views.excluir_produto, name='excluir_produto'),
    path('listar_categorias', views.listar_categorias, name='listar_categorias'),
    path('cadastrar_categoria', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('excluir_categoria/<int:id>', views.excluir_categoria, name='excluir_categoria'),
    path('alterar_produto/<int:id>', views.alterar_produto, name='alterar_produto'),
    path('salvar_avaliacao/<int:id_produto>', views.salvar_avaliacao, name='salvar_avaliacao'),
    path('alterar_imagem_principal/<int:id_produto>', views.alterar_imagem_principal, name='alterar_imagem_principal'),
    path('incluir_imagens/<int:id_produto>', views.incluir_imagens, name='incluir_imagens'),
    path('excluir_imagem/<int:id_imagem>/<int:id_produto>', views.excluir_imagem, name='excluir_imagem'),
    path('excluir_imagem_principal/<int:id_produto>', views.excluir_imagem_principal, name='excluir_imagem_principal'),
    path('excluir_avaliacao/<int:id_avaliacao>/<int:id_produto>', views.excluir_avaliacao, name='excluir_avaliacao'),
    path('atualizar_especificacao/<int:id>', views.atualizar_especificacao, name='atualizar_especificacao'),
    path('teste/', views.teste, name='teste'),
]