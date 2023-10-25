from .models import Saida, RelatorioEntradaSaida

from rest_framework import serializers


class SaidaSerializer(serializers.ModelSerializer):

    data_saida_formatada = serializers.SerializerMethodField()

    class Meta:
        model = Saida
        fields = ('tipo_de_despesa', 'valor_despesa', 'data_saida_formatada')

    def get_data_saida_formatada(self, obj):
        return obj.data_saida.strftime('%d/%m/%Y')
    

class LogsSerializer(serializers.ModelSerializer):

    data_log_formatada = serializers.SerializerMethodField()

    class Meta:
        model = RelatorioEntradaSaida
        fields = ('tipo', 'valor', 'data_log_formatada')

    def get_data_log_formatada(self, obj):
        return obj.data.strftime('%d/%m/%Y')