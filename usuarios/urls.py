from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('excluir_usuario/<int:id>', views.excluir_usuario, name='excluir_usuario'),
    path('ver_usuario/<int:id>', views.ver_usuario, name='ver_usuario'),
    path('conceder_permissao', views.conceder_permissao, name='conceder_permissao'),
    path('atualizar_usuario/<int:id>', views.atualizar_usuario, name='atualizar_usuario')
]