from rest_framework import serializers
from .models import Carrinho


class CarrinhoSerializer(serializers.ModelSerializer):
    produtos = serializers.ListField(child=serializers.CharField())
    quantidades = serializers.ListField(child=serializers.IntegerField())  # Adicione este campo
    valores = serializers.ListField(child=serializers.DecimalField(decimal_places=2, max_digits=10))  # Adicione este campo

    class Meta:
        model = Carrinho
        fields = ['user','id', 'produtos_nomes', 'valor_da_compra', 'quantidade_produtos', 'data_compra', 'produtos', 'quantidades', 'valores']
