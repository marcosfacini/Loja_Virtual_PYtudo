from dataclasses import fields
from django import forms
from .models import Usuarios
from phonenumber_field.formfields import PhoneNumberField

class CadastroUsuario(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()

class AtualizarUsuario(forms.Form):
    nome = forms.CharField(max_length=40)
    cpf = forms.CharField(max_length=14)
    data_de_nascimento = forms.DateField()
    celular = PhoneNumberField()
    endereco = forms.CharField(max_length=50)
    numero_endereco = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=50, required=False)
    bairro = forms.CharField(max_length=30)
    cidade = forms.CharField(max_length=30)
    estado = forms.ChoiceField(choices=Usuarios.ESTADOS_BRASILEIROS, label='Estado')



        
    


    
    


