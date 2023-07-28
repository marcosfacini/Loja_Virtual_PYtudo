from dataclasses import fields
from django import forms
from .models import CupomDesconto

class FormCupomDesconto(forms.ModelForm):
    class Meta:
        model = CupomDesconto
        fields = '__all__'
