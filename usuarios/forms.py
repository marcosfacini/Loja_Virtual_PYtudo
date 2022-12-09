from dataclasses import fields
from django import forms
from .models import Usuarios

class CadastroUsuario(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'