from django.urls import path
from . import views

urlpatterns = [
    path('criar_gerente/', views.criar_gerente, name="criar_gerente"),
    path('salvar_gerente/', views.salvar_gerente, name='salvar_gerente'),
    path('criar_gestor/', views.criar_gestor, name="criar_gestor"),
    path('salvar_gestor/', views.salvar_gestor, name='salvar_gestor'),
    path('adm_estoque/', views.adm_estoque, name='adm_estoque'),
   
]

# admin:
# marcola@gmail.com 
# marcola

# gestor:
# gestor@gmail.com
# mr.m1880