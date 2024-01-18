from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name="checkout"),
    path('get_chave_publica/', views.get_chave_publica, name="get_chave_publica"),
    path('processar_metodo_pagamento/', views.processar_metodo_pagamento, name="processar_metodo_pagamento"),
    path('notificacao_pagseguro/', views.notificacao_pagseguro, name="notificacao_pagseguro"),

]