from dataclasses import fields
from django import forms
from .models import Produtos

class CadastroProduto(forms.ModelForm):
    class Meta:
        model = Produtos
        fields = '__all__'