from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from relatorios.serializer import LogsSerializer
from .forms import SaidaForm
from .models import Saida, RelatorioEntradaSaida
from caixa.models import Carrinho
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Saida
from caixa.models import Carrinho
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum




@login_required(login_url="login")
def relatorio(request):

    data_inicial_str = request.GET.get('data_inicial')
    data_final_str = request.GET.get('data_final')

    current_month = timezone.now().month
    current_year = timezone.now().year

    
    logs = RelatorioEntradaSaida.objects.all().order_by('-data')
    
    total_entradas = RelatorioEntradaSaida.objects.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum']
    total_saidas = RelatorioEntradaSaida.objects.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum']

    logs = RelatorioEntradaSaida.objects.filter(data__month=current_month, data__year=current_year).order_by('-data')

    if data_final_str:
        logs = logs.filter(data__date__gte=data_inicial_str)
    if data_final_str:
        logs = logs.filter(data__date__lte=data_final_str)


    total_entradas_mensal = logs.filter(tipo='entrada').aggregate(Sum('valor'))['valor__sum']
    total_saidas_menasl = logs.filter(tipo='saida').aggregate(Sum('valor'))['valor__sum']

    # Pagination
    page_number = request.GET.get('page', 1)
    items_per_page = 10
    paginator = Paginator(logs, items_per_page)
    page_logs = paginator.get_page(page_number)

    context = {
        'url_full': request.build_absolute_uri(),
        'logs': page_logs,
        'total_entradas': total_entradas or 0,
        'total_entradas_mensal': round(total_entradas_mensal, 2) or 0,
        'total_saidas_mensal': round(total_saidas_menasl, 2) or 0,
        'total_saidas': total_saidas or 0, 
        'data_inicial': data_inicial_str,
        'data_final': data_final_str,
        
    }

    return render(request, 'html/relatorio.html', context)



@login_required(login_url="login")
def add_despesas(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            response_data = {'success': 'Despesa cadastrada com sucesso!'}
            return JsonResponse(response_data)
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
    
@login_required(login_url="login")
def deletar_relatorio(request, id):
    
    if request.method == 'POST':    
        relatorio = get_object_or_404(RelatorioEntradaSaida, id=id)
        relatorio.delete()
        return redirect('relatorio')
    
