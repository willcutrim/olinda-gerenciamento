import json
from django.shortcuts import get_object_or_404, redirect, render
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





def home(request):
    return render(request, 'html/index.html')


def historico_de_vendas(request):
    # Obtenha as datas de início e fim dos parâmetros da solicitação GET
    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')

    # Converta as strings de data para objetos datetime, se fornecidas

    vendas = Carrinho.objects.all().order_by('-data_compra')
    
    if data_inicial_str:
        vendas = vendas.filter(data_compra__date__gte=data_inicial_str)
    if data_final_str:
        vendas = vendas.filter(data_compra__date__lte=data_final_str)

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

    # Passe as datas iniciais e finais para o contexto do modelo
    context = {
        "vendas": vendas,
        "calc_list": total_value,
        "data_inicial": data_inicial_str,
        "data_final": data_final_str,
    }

    return render(request, 'html/historico_vendas.html', context)




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
        print(request.data)
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


def deletar_venda(request, id):

    if request.method == 'POST':    
        carrinho = get_object_or_404(Carrinho, id=id)
        carrinho.delete()
        return redirect('historico-vendas')