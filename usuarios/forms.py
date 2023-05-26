from dataclasses import fields
from django import forms
from .models import Usuarios

class CadastroUsuario(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()
        
    


    
    


