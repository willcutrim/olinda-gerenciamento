from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from relatorios.serializer import LogsSerializer, SaidaSerializer
from .forms import SaidaForm
from .models import Saida, RelatorioEntradaSaida
from caixa.models import Carrinho

from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .models import Saida
from caixa.models import Carrinho
from django.core.paginator import Paginator


from datetime import datetime


def relatorio(request):
    
    logs = RelatorioEntradaSaida.objects.all().order_by('-data')
    
    page_number = request.GET.get('page', 1)
    items_per_page = 10

    logs = Paginator(logs, items_per_page)
    page_logs = logs.get_page(page_number)
    return render(request, 'html/relatorio.html', {'logs': page_logs})



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
        
        logs_saida = RelatorioEntradaSaida.objects.filter(tipo='saida', data__month=mes_atual, data__year=ano_atual)
        logs_data = RelatorioEntradaSaida.objects.filter(data__month=mes_atual, data__year=ano_atual)
        logs_entrada = RelatorioEntradaSaida.objects.filter(tipo='entrada', data__month=mes_atual, data__year=ano_atual)

        serializer_saida = LogsSerializer(logs_saida, many=True)
        serializer_data = LogsSerializer(logs_data, many=True)
        serializer_entrada = LogsSerializer(logs_entrada, many=True)
        
        data = {
            'saida': serializer_saida.data,
            'entrada': serializer_entrada.data,
            'logs_data': serializer_data.data
        }
        return Response(data)