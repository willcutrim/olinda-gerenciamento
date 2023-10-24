from django.contrib import admin
from .models import Categoria, Fornecedor, Produto

class AdminProduto(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'tamanho', 'preco']
    list_editable = ['tamanho', 'preco', 'categoria']
    

admin.site.register(Produto, AdminProduto)
admin.site.register(Fornecedor)
admin.site.register(Categoria)