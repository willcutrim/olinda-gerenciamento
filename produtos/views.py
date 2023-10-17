from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .forms import CategoriaForm, FornecedorForm, ProdutoForm
from produtos.models import Produto

class GetAllProducts(View):
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        data = [{'nome': produto.nome, 'descricao': produto.descricao, 'preco': produto.preco} for produto in produtos]
        return JsonResponse({'status': 200, 'produtos': data})
    
def produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'html/produtos.html', {'produtos': produtos})


def cadastro_de_produtos(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro-produto')
    else:
        form = ProdutoForm()
    return render(request, 'html/cadastrar_produtos.html', {'form': form})