from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

import caixa
# from caixa.models import Carrinho

class Saida(models.Model):
    saida_status = models.CharField(max_length=120, default='saida')
    tipo_de_despesa = models.CharField(
        max_length=150, 
        verbose_name='Tipo de Despesa (Ex. Conta de energia)')
    descricao = models.TextField(max_length=250, verbose_name='Descrição (OPCIONAL)')
    valor_despesa = models.DecimalField(decimal_places=2, max_digits=10, default=0, blank=True, verbose_name='Valor da despesa')
    data_saida = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Saida'
        verbose_name_plural = 'Saidas'

    def __str__(self):
        return self.tipo_de_despesa
    

    def data_saida_formatada(self):
        return self.data_saida.strftime('%d/%m/%Y %H:%M')
    

class RelatorioEntradaSaida(models.Model):
    id_do_movimento = models.CharField(max_length=150)
    tipo = models.CharField(max_length=150)
    descricao = models.TextField(max_length=250)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tipo
    
    def data_log_formatada(self):
        return self.data.strftime('%d/%m/%Y - %H:%M')



@receiver(post_save, sender=Saida)
def create_relatorio_entrada_saida(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            id_do_movimento=instance.id,
            tipo=instance.saida_status,
            descricao=instance.descricao,
            valor=instance.valor_despesa,
            data=instance.data_saida
        )
    

@receiver(pre_delete, sender=RelatorioEntradaSaida)
def deletar_relatorio_entrada(sender, instance, **kwargs):
    try:
        relatorio = caixa.models.Carrinho.objects.get(id=instance.id_do_movimento)
        relatorio.delete()
    except caixa.models.Carrinho.DoesNotExist:
        pass
    except Exception as e:
        #
        print(f"Erro ao excluir relatório: {e}")