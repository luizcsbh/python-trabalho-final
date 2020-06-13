from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from ..models import Despesa, Receita

@require_http_methods(["GET"])
def despesas(request):
    despesasPendentes = Despesa.objects.filter(situacao='AP')
    context = GetDespesaContext(despesasPendentes , '')
    
    return render(request, 'relatorioDespesas.html', context)


@require_http_methods(["GET"])
def receitas(request):
    receitasPendentes = Receita.objects.filter(situacao='AR')
    context = GetReceitaContext(receitasPendentes , '')
    
    return render(request, 'relatorioReceitas.html', context)


@require_http_methods(["POST"])    
@csrf_exempt
def despesasFiltro(request):
    dataFiltro = request.POST['data_filtro']
    
    despesasPendentes = Despesa.objects.filter(situacao='AP', data_vencimento__lte=dataFiltro)
    context = GetDespesaContext(despesasPendentes, dataFiltro)

    return render(request, 'relatorioDespesas.html', context)


@require_http_methods(["POST"])    
@csrf_exempt
def receitasFiltro(request):
    dataFiltro = request.POST['data_filtro']
    
    receitasPendentes = Receita.objects.filter(situacao='AR', data_expectativa__lte=dataFiltro)
    context = GetReceitaContext(receitasPendentes, dataFiltro)

    return render(request, 'relatorioReceitas.html', context)


def GetDespesaContext(despesasPendentes, dateMax):
    valorTotal = 0
    for despesa in despesasPendentes:
        dtVencimento = '%s/%s/%s' % (despesa.data_vencimento.strftime("%d"), despesa.data_vencimento.strftime("%m"), despesa.data_vencimento.strftime("%Y"))
        despesa.data_vencimento = dtVencimento
        valorTotal = valorTotal + despesa.valor
    
    dateMaxBr = ""
    if(dateMax != ""):
        dateTemp = datetime.strptime(dateMax, '%Y-%m-%d').date()
        dateMaxBr = '%s/%s/%s' % (dateTemp.strftime("%d"), dateTemp.strftime("%m"), dateTemp.strftime("%Y"))

    context = {'despesas' : despesasPendentes,
                'valorTotal' : valorTotal,
                'dateMax' : dateMax,
                'dateMaxBr' : dateMaxBr}

    return context


def GetReceitaContext(receitasPendentes, dateMax):
    valorTotal = 0
    for receita in receitasPendentes:
        dtExpectativa = '%s/%s/%s' % (receita.data_expectativa.strftime("%d"), receita.data_expectativa.strftime("%m"), receita.data_expectativa.strftime("%Y"))
        receita.data_expectativa = dtExpectativa
        valorTotal = valorTotal + receita.valor
    
    dateMaxBr = ""
    if(dateMax != ""):
        dateTemp = datetime.strptime(dateMax, '%Y-%m-%d').date()
        dateMaxBr = '%s/%s/%s' % (dateTemp.strftime("%d"), dateTemp.strftime("%m"), dateTemp.strftime("%Y"))

    context = {'receitas' : receitasPendentes,
                'valorTotal' : valorTotal,
                'dateMax' : dateMax,
                'dateMaxBr' : dateMaxBr}

    return context
