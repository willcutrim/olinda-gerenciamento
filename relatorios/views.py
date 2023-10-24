from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from relatorios.serializer import SaidaSerializer
from .forms import SaidaForm
from .models import Saida
from caixa.models import Carrinho

from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .models import Saida
from caixa.models import Carrinho
from django.core.paginator import Paginator


from datetime import datetime


def relatorio(request):
    despesas = Saida.objects.all()
    entradas = Carrinho.objects.all()
    
    is_arrow_up = True
    for despesa in despesas:
        despesa.is_up_arrow = is_arrow_up
        is_arrow_up = not is_arrow_up

    is_arrow_up = True
    for entrada in entradas:
        entrada.is_up_arrow = is_arrow_up
        is_arrow_up = not is_arrow_up

    page_number = request.GET.get('page', 1)
    items_per_page = 10
    despesas_paginator = Paginator(despesas, items_per_page)
    entradas_paginator = Paginator(entradas, items_per_page)

    despesas_page = despesas_paginator.get_page(page_number)
    entradas_page = entradas_paginator.get_page(page_number)

    return render(request, 'html/relatorio.html', {'despesas_page': despesas_page, 'entradas_page': entradas_page})



def add_despesas(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_relatorio')
    else:
        form = SaidaForm()
    return render(request, 'html/add_despesas.html', {'form': form})



class DataRelatorio(View):


    def get(self, request):
        saidas = Saida.objects.all()
        carrinho = Carrinho.objects.all()

        data = {
            'saidas': sum(saida.valor_despesa for saida in saidas),
            'carrinho': sum(venda.valor_da_compra for venda in carrinho),
        }
        
        return JsonResponse(data)
    


class DataAllRelatorio(APIView):

    
    def get(self, request):

        hoje = datetime.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        saidas = Saida.objects.filter(data_saida__month=mes_atual, data_saida__year=ano_atual)

        serializer_saida = SaidaSerializer(saidas, many=True)
        
        return Response(serializer_saida.data)