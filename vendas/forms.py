from dataclasses import fields
from django import forms
from .models import CupomDesconto

class CupomDesconto(forms.ModelForm):
    class Meta:
        model = CupomDesconto
        fields = '__all__'
