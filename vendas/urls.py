from django.urls import path
from . import views

urlpatterns = [
    path('vender_produto/<int:id>', views.vender_produto, name="vender_produto"),
    
]