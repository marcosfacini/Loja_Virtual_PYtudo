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
]