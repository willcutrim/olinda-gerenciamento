from django.db import models

TIPO_DESPESA_CHOICES = [
    ('conta_luz', 'Conta de Luz'),
    ('conta_agua', 'Conta de Água'),
    ('conta_internet', 'Conta de Internet'),
    ('outras_despesas', 'Outras Despesas'),
    # Adicione outros tipos de despesas conforme necessário
]

class Saida(models.Model):
    tipo_de_despesa = models.CharField(
        max_length=150, 
        choices=TIPO_DESPESA_CHOICES, 
        default='outras_despesas', 
        verbose_name='Tipo de Despesa')
    valor_despesa = models.DecimalField(decimal_places=2, max_digits=10, default=0, blank=True, verbose_name='Valor da despesa')
    data_saida = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Saida'
        verbose_name_plural = 'Saidas'

    def __str__(self):
        return self.tipo_de_despesa
    

    def data_saida_formatada(self):
        return self.data_saida.strftime('%d/%m/%Y %H:%M')