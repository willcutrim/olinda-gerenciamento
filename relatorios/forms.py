from django import forms
from .models import Saida

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = '__all__'