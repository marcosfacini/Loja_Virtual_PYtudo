from dataclasses import fields
from django import forms
from .models import Categoria
from django.forms.widgets import ClearableFileInput
from ckeditor_uploader.fields import RichTextUploadingFormField

class CadastrarProduto(forms.Form):
    nome = forms.CharField(max_length=40)
    descricao = forms.CharField(max_length=100000, required=False)
    preco_de_custo = forms.CharField(max_length=11)
    preco = forms.CharField(max_length=11)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=False)
    marca = forms.CharField(max_length=50, required=False)
    cor = forms.CharField(max_length=30, required=False) 
    quantidade = forms.IntegerField()
    imagem_principal = forms.ImageField(required=False)
    outras_imagens = forms.ImageField(widget=ClearableFileInput(attrs={'multiple':True}), required=False)
    especificacao = RichTextUploadingFormField(required=False)
    frete_gratis = forms.BooleanField(required=False)
    altura = forms.CharField(max_length=10, required=False)
    largura = forms.CharField(max_length=10, required=False)
    profundidade = forms.CharField(max_length=10, required=False)
    peso = forms.CharField(max_length=10, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()

class AtualizarEspecificacao(forms.Form):
    especificacao = RichTextUploadingFormField()
