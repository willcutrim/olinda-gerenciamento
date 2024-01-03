from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CategoriaForm, FornecedorForm, ProdutoForm
from produtos.models import Categoria, Produto
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import UpdateView

class GetAllProducts(View):
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        data = [{'nome': produto.nome, 'descricao': produto.descricao, 'preco': produto.preco} for produto in produtos]
        return JsonResponse({'status': 200, 'produtos': data})
    
def produtos(request):
    produtos = Produto.objects.all()
    paginator = Paginator(produtos, 10)

    page = request.GET.get('page')

    try:
        produtos = paginator.get_page(page)
    except PageNotAnInteger:
        produtos = paginator.get_page(1)
    except EmptyPage:
        produtos = paginator.get_page(paginator.num_pages)

    return render(request, 'html/produtos.html', {'produtos': produtos})


def cadastro_de_produtos(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            response_data = {'success': 'Produto cadastrado com suceosso!'}
            return JsonResponse(response_data)
    else:
        form = ProdutoForm()
    return render(request, 'html/cadastrar_produtos.html', {'form': form})


def create_category(request):
    if request.method == 'POST':
        nome_categoria = request.POST.get('nome_caegoria')
        
        # Create the category in the database (you should handle validation and error checks here)
        categoria = Categoria.objects.create(nome_caegoria=nome_categoria)
        
        return JsonResponse({'message': 'Categoria cadastrada com sucesso!'})
    else:
        return JsonResponse({'error': 'Método inválido'}, status=400)
    

def deletar_produto(request, id):
   
    if request.method == 'POST':    
        produto = get_object_or_404(Produto, id=id)
        produto.delete()
        return redirect('produtos')
    

class ProdutoUpdateView(UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = 'html/atualizar_produtos.html'  # Create a template for updating products
    success_url = '/produtos/'  # Redirect to this URL upon successful update

    def form_valid(self, form):
        # You can perform additional actions when the form is successfully validated and saved.
        # For example, you might want to log the user who made the update.
        # Here's a basic example:
        form.instance.updated_by = self.request.user
        return super().form_valid(form)