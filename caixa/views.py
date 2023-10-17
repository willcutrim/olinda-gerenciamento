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

def home(request):
    return render(request, 'html/index.html')


def historico_de_vendas(request):
    vendas = Carrinho.objects.all()
    calc_list = []
    
    for venda in vendas:
        calc_list.append(venda.valor_da_compra)

    print(sum(calc_list))
    return render(request, 'html/historico_vendas.html', {"vendas": vendas, 'calc_list': sum(calc_list)})


def caixa(request):
    return render(request, 'html/caixa.html')


class PostFrenteCaixa(APIView):
    def post(self, request):
        serializer = CarrinhoSerializer(data=request.data)
        if serializer.is_valid():
            produtos = serializer.validated_data.pop('produtos', [])
            quantidades = serializer.validated_data.pop('quantidades', [])  
            valores = serializer.validated_data.pop('valores', [])  
            print(valores)
            carrinho = Carrinho.objects.create(**serializer.validated_data, produtos_nomes=','.join(produtos), produtos_quantidades=','.join(map(str, quantidades)), produtos_valores=','.join(map(str, valores)))

            response_serializer = CarrinhoSerializer(carrinho)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

