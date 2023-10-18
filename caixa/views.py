import json
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from caixa.models import Carrinho
from caixa.serializer import CarrinhoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from produtos.models import Produto
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from produtos.serializer import PodutoSerializer




def home(request):
    return render(request, 'html/index.html')


def historico_de_vendas(request):
    vendas = Carrinho.objects.all()
    
    total_value = sum(venda.valor_da_compra for venda in vendas)
    items_per_page = 10 

   
    paginator = Paginator(vendas, items_per_page)
    
    
    page = request.GET.get('page')

    try:
        
        vendas = paginator.get_page(page)
    except PageNotAnInteger:
        
        vendas = paginator.get_page(1)
    except EmptyPage:
        
        vendas = paginator.get_page(paginator.num_pages)

    

    return render(request, 'html/historico_vendas.html', {"vendas": vendas, 'calc_list': total_value})



def caixa(request):
    produtos = Produto.objects.all()
    return render(request, 'html/caixa.html', {'produtos': produtos})

def get_product_price(request):
    
    product_name = request.GET.get('product')
    try:
        product = Produto.objects.get(nome=product_name)
        price = product.preco
        return JsonResponse({'preco': price})
    except Produto.DoesNotExist:
        return JsonResponse({'preco': 0.00})
    

class PostFrenteCaixa(APIView):
    def post(self, request):
        serializer = CarrinhoSerializer(data=request.data)
        
        if serializer.is_valid():
            produtos = serializer.validated_data.pop('produtos', [])
            quantidades = serializer.validated_data.pop('quantidades', [])
            valores = serializer.validated_data.pop('valores', [])
            teste_calc = sum(i for i in quantidades)
            print(teste_calc)
            carrinho = Carrinho.objects.create(
                **serializer.validated_data,
                produtos_nomes=','.join(produtos),
                quantidade_produtos=teste_calc,
                produtos_valores=','.join(map(str, valores)),
                valor_da_compra=request.data['valorTotal'],
            )
            response_serializer = CarrinhoSerializer(carrinho)
            print(response_serializer.data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def create_carrinho(request):
#     if request.method == 'POST':
#         data = request.POST  # Assuming you're sending data via POST
#         produtos_nomes = data.get('produtos_nomes', '')
#         produtos_quantidades = data.get('produtos_quantidades', '')
#         produtos_valores = data.get('produtos_valores', '')
#         valor_da_compra = data.get('valor_da_compra', 0)
#         quantidade_produtos = data.get('quantidade_produtos', '')

#         # Create a new Carrinho object with the received data
#         carrinho = Carrinho.objects.create(
#             produtos_nomes=produtos_nomes,
#             produtos_quantidades=produtos_quantidades,
#             produtos_valores=produtos_valores,
#             valor_da_compra=valor_da_compra,
#             quantidade_produtos=quantidade_produtos,
#         )

#         return JsonResponse({'message': 'Carrinho created successfully'})

#     return JsonResponse({'message': 'Invalid request'}, status=400)
