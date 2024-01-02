from django import forms
from .models import Saida

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ('tipo_de_despesa', 'valor_despesa', 'descricao')