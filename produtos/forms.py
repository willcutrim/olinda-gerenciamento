from django import forms
from .models import Categoria, Fornecedor, Produto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nome_caegoria',)

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ('nome_fornecedor', 'contato', 'email')

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'descricao', 'categoria', 'preco', 'tamanho', 'cor', 'marca', 'fornecedor',)

