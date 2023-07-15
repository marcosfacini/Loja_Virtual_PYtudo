from django.urls import path
from . import views

urlpatterns = [
    path('vender_produto/<int:id>', views.vender_produto, name="vender_produto"),
    path('adicionar_na_lista_desejo/<int:id>', views.adicionar_na_lista_desejo, name='adicionar_na_lista_desejo'),
    path('ver_lista_desejo/', views.ver_lista_desejo, name='ver_lista_desejo'),
    path('esvaziar_lista_desejo/', views.esvaziar_lista_desejo, name='esvaziar_lista_desejo'),
    path('criar_historico_da_venda/', views.criar_historico_da_venda, name='criar_historico_da_venda'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('adicionar_ao_carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('adicionar_quantidade_no_carrinho/', views.adicionar_quantidade_no_carrinho, name='adicionar_quantidade_no_carrinho'),
    
]