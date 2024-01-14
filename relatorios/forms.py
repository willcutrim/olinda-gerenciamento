from django import forms
from .models import Saida

class SaidaForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ('tipo_de_despesa', 'valor_despesa', 'descricao')


    def save(self, commit=True, user=None, *args, **kwargs):
        # Atribuir o usuário logado ao campo 'user'
        instance = super().save(commit=False, *args, **kwargs)
        instance.user = user
        if commit:
            instance.save()
        return instance