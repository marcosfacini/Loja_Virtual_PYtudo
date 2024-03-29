from django.urls import path
from . import views

urlpatterns = [
    path('adicionar_na_lista_desejo/<int:id>', views.adicionar_na_lista_desejo, name='adicionar_na_lista_desejo'),
    path('ver_lista_desejo/', views.ver_lista_desejo, name='ver_lista_desejo'),
    path('excluir_item_da_lista/<int:id_produto>/', views.excluir_item_da_lista, name='excluir_item_da_lista'),
    path('esvaziar_lista_desejo/', views.esvaziar_lista_desejo, name='esvaziar_lista_desejo'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('adicionar_quantidade_no_carrinho/', views.adicionar_quantidade_no_carrinho, name='adicionar_quantidade_no_carrinho'),
    path('excluir_do_carrinho/<int:id_produto>/', views.excluir_do_carrinho, name='excluir_do_carrinho'),
    path('criar_cupom/', views.criar_cupom, name='criar_cupom'),
    path('validar_cupom/', views.validar_cupom, name='validar_cupom'),
    path('retirar_cupom_da_session/', views.retirar_cupom_da_session, name='retirar_cupom_da_session'),
    
]