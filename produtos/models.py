from django.db import models

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
    codigo_de_barras = models.CharField(max_length=150, null=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tamanho = models.CharField(max_length=10)
    cor = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, blank=True)
    destaque = models.BooleanField(default=False)
    em_promocao = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

