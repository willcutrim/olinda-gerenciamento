from .models import Saida

from rest_framework import serializers


class SaidaSerializer(serializers.ModelSerializer):

    data_saida_formatada = serializers.SerializerMethodField()

    class Meta:
        model = Saida
        fields = ('tipo_de_despesa', 'valor_despesa', 'data_saida_formatada')

    def get_data_saida_formatada(self, obj):
        return obj.data_saida.strftime('%d/%m/%Y')