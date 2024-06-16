from django.db import models
import uuid
class Categoria(models.Model):
    nome_caegoria = models.CharField(max_length=150)
    def __str__(self):
        return self.nome_caegoria
    
class Fornecedor(models.Model):
    nome_fornecedor = models.CharField(max_length=150)
    contato = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.nome_fornecedor

class Produto(models.Model):
    # codigo_de_barras = models.UUIDField(default=uuid.uuid4, unique=True)
    nome = models.CharField(max_length=100, verbose_name="Nome do Produto*")
    descricao = models.TextField(null=True, blank=True, verbose_name="Descrição")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    quantidade_estoque = models.IntegerField(null=True, blank=True, verbose_name="Quantidade em Estoque")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço*")
    tamanho = models.CharField(max_length=10, null=True, blank=True, verbose_name="Tamanho")
    cor = models.CharField(max_length=50, null=True, blank=True, verbose_name="Cor")
    marca = models.CharField(max_length=50, null=True, blank=True, verbose_name="Marca")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, blank=True)
    destaque = models.BooleanField(default=False, null=True, blank=True)
    em_promocao = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.nome

