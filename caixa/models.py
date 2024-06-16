from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from relatorios.models import RelatorioEntradaSaida
from produtos.models import Produto

class Carrinho(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    status_entrada = models.CharField(max_length=120, default='entrada')
    produtos_nomes = models.CharField(max_length=200, blank=True)
    produtos_quantidades = models.CharField(max_length=200, blank=True)
    produtos_valores = models.CharField(max_length=200, blank=True) 
    valor_da_compra = models.DecimalField(decimal_places=2, max_digits=10, default=0, blank=True)
    quantidade_produtos = models.CharField(max_length=150, null=True)
    data_compra = models.DateTimeField(auto_now_add=True)

    def adicionar_produto_por_nome(self, nome_produto, quantidade, valor):
        if not self.produtos_nomes:
            self.produtos_nomes = nome_produto
            self.produtos_quantidades = str(quantidade)
            self.produtos_valores = str(valor)
        else:
            produtos_nomes_list = self.produtos_nomes.split(',')
            produtos_quantidades_list = self.produtos_quantidades.split(',')
            produtos_valores_list = self.produtos_valores.split(',')

            if nome_produto in produtos_nomes_list:
                index = produtos_nomes_list.index(nome_produto)
                produtos_quantidades_list[index] = str(int(produtos_quantidades_list[index]) + quantidade)
                produtos_valores_list[index] = str(float(produtos_valores_list[index]) + valor)
            else:
                produtos_nomes_list.append(nome_produto)
                produtos_quantidades_list.append(str(quantidade))
                produtos_valores_list.append(str(valor))

            self.produtos_nomes = ','.join(produtos_nomes_list)
            self.produtos_quantidades = ','.join(produtos_quantidades_list)
            self.produtos_valores = ','.join(produtos_valores_list)

        self.valor_da_compra = sum([float(valor) for valor in produtos_valores_list])
        self.quantidade_produtos = str(sum([int(quantidade) for quantidade in produtos_quantidades_list]))
        self.save()

    def obter_nomes_produtos(self):
        if self.produtos_nomes:
            return self.produtos_nomes.split(', ')
        else:
            return []
    
    def __str__(self):
        return self.produtos_nomes
    

@receiver(post_save, sender=Carrinho)
def create_relatorio_entrada_saida(sender, instance, created, **kwargs):
    if created:
        RelatorioEntradaSaida.objects.create(
            user=instance.user,
            id_do_movimento=instance.id,
            tipo=instance.status_entrada,
            descricao="Venda",
            valor=instance.valor_da_compra,
            data=instance.data_compra
        )


@receiver(pre_delete, sender=Carrinho)
def deletar_relatorio_entrada(sender, instance, **kwargs):
    try:
        relatorio = RelatorioEntradaSaida.objects.get(id_do_movimento=instance.id)
        relatorio.delete()
    except RelatorioEntradaSaida.DoesNotExist:
        pass
    except Exception as e:
        #
        print(f"Erro ao excluir relatório: {e}")


@receiver(post_save, sender=Carrinho)
def update_estoque(sender, instance, **kwargs):
    try:
        for nome_produto, quantidade, valor in zip(instance.produtos_nomes.split(', '), instance.produtos_quantidades.split(', '), instance.produtos_valores.split(', ')):
            produto = Produto.objects.get(nome=nome_produto)
            if instance.status_entrada == 'entrada':
                produto.quantidade_estoque -= int(quantidade)
                produto.save()
            else:
                produto.quantidade_estoque -= int(quantidade)
                produto.save()
    except Exception as e:
        #
        print(f"Erro ao atualizar estoque: {e}")