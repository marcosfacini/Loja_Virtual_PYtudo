from django.urls import path
from . import views

urlpatterns = [
    path('info_adicional_usuario/', views.info_adicional_usuario, name="info_adicional_usuario"),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('excluir_usuario/<int:id>', views.excluir_usuario, name='excluir_usuario'),
    path('ver_usuario/<int:id>', views.ver_usuario, name='ver_usuario'),
    path('atualizar_usuario/<int:id>', views.atualizar_usuario, name='atualizar_usuario'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('usuario_atualiza_cadastro/', views.usuario_atualiza_cadastro, name='usuario_atualiza_cadastro'),
    path('alteracoes_usuario/', views.alteracoes_usuario, name='alteracoes_usuario'),
    path('meus_pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('ver_pedido/<int:id>', views.ver_pedido, name='ver_pedido'),
]