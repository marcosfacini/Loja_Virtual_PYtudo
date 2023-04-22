from django.urls import path
from . import views

urlpatterns = [
    path('vender_produto/<int:id>', views.vender_produto, name="vender_produto"),
    path('adicionar_no_carrinho/<int:id>', views.adicionar_no_carrinho, name='adicionar_no_carrinho'),
    path('ver_carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('esvaziar_carrinho/', views.esvaziar_carrinho, name='esvaziar_carrinho'),
    
]