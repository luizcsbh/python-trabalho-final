from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..models import Conf, Despesa, Receita
import operator

@require_http_methods(["GET", "POST"])
@csrf_exempt
def index(request):
    if(request.method=="GET"):
        context = carregaContextFluxo()
        return render(request, 'index.html', context)
    elif(request.method=="POST"):
        result = Conf.objects.all()
        message = 'Saldo inicial criado com sucesso!'
        if(result.count() > 0):
            message = 'Saldo inicial alterado com sucesso!'
            for confObj in result:
                confObj.delete()

        conf = Conf(saldoInicial=request.POST['saldoInicial'])
        conf.save()
        context = carregaContextFluxo()
        context["message"] = message
        return render(request, 'index.html', context)

# carrega o context do fluxo de caixa
def carregaContextFluxo():
    saldoInicial = carregaSaldoInicial()
    context = {'saldoInicial' : saldoInicial}
    if(saldoInicial != None):
        saldoAtual = saldoInicial

        fluxo = initFluxo(saldoInicial)
        for periodo in fluxo:
            saldoAtual = fluxo[periodo]['saldoFinal']
            break

        context['fluxo'] = fluxo
        context['saldoAtual'] = saldoAtual

    #print(f"""context= {context}""")
    return context

# se existir carrega o saldo inicial
def carregaSaldoInicial():
    saldoInicial = None
    searchSaldoInicial = Conf.objects.all()
    if(searchSaldoInicial.count() >= 1):
        saldoInicial = searchSaldoInicial[0].saldoInicial

    return saldoInicial

# inicializa e adiciona as informações do fluxo de caixa, com as informações de todos os meses
def initFluxo(saldoInicial):
    if(saldoInicial == None):
        return {}

    fluxo = {}
    fluxo = createOrderPeriodos(fluxo)
    fluxo = setResumoReceitas(fluxo)
    fluxo = setResumoDespesas(fluxo)
    fluxo = setSaldoIniFinLuc(fluxo, saldoInicial)
    fluxo = setDespesasOrder(fluxo)
    fluxo = setReceitasOrder(fluxo)
    fluxo = setSaldoAcumulado(fluxo, saldoInicial)

    return fluxo

# inicializa o fluxo de um mês vazio
def createFluxoVazio(fluxo, periodo):
    fluxo[periodo] = {  'saldoReceber' : 0, 
                        'saldoRecebido' : 0, 
                        'saldoPagar' : 0, 
                        'saldoPago' : 0,
                        'saldoInicial' : 0,
                        'saldoFinal' : 0,
                        'lucratividade' : 0,
                        'saldoPrevisto' : 0,
                        "receitas" : [],
                        "despesas" : []}
    return fluxo

# cria a ordem inversa dos periodos para ser apresentada na página
def createOrderPeriodos(fluxo):
    lstDates = []
    resultReceitas1 = Receita.objects.order_by('-data_recebimento')
    for receita in resultReceitas1:
        if(receita.data_recebimento):
            if(receita.data_recebimento not in lstDates):
                lstDates.append(receita.data_recebimento)

    resultReceitas2 = Receita.objects.order_by('-data_expectativa')
    for receita in resultReceitas2:
        if(receita.data_expectativa):
            if(receita.data_expectativa not in lstDates):
                lstDates.append(receita.data_expectativa)

    resultDespesas1 = Despesa.objects.order_by('-data_pagamento')
    for despesa in resultDespesas1:
        if(despesa.data_pagamento):
            if(despesa.data_pagamento not in lstDates):
                lstDates.append(despesa.data_pagamento)

    resultDespesas2 = Despesa.objects.order_by('-data_vencimento')
    for despesa in resultDespesas2:
        if(despesa.data_vencimento):
            if(despesa.data_vencimento not in lstDates):
                lstDates.append(despesa.data_vencimento)

    #print(f"""lstDates= {lstDates}""")
    sorted_list = sorted(lstDates)
    for dateCheck in reversed(sorted_list):
        periodo = '%s/%s' % (dateCheck.strftime("%m"), dateCheck.strftime("%Y"))
        if periodo not in fluxo:
            fluxo = createFluxoVazio(fluxo, periodo)
            #print(f"""periodo= {periodo}""")
    
    return fluxo

# recupera as seguintes informações do mês: saldo recebido, saldo a receber
def setResumoReceitas(fluxo):
    resultReceitas = Receita.objects.all().order_by('-data_expectativa')
    for receita in resultReceitas:
        if(receita.data_recebimento):
            periodo = '%s/%s' % (receita.data_recebimento.strftime("%m"), receita.data_recebimento.strftime("%Y"))
        else:
            periodo = '%s/%s' % (receita.data_expectativa.strftime("%m"), receita.data_expectativa.strftime("%Y"))

        if(receita.situacao == "PR"):
            fluxo[periodo]['saldoRecebido'] = fluxo[periodo]['saldoRecebido'] + receita.valor
        else:
            fluxo[periodo]['saldoReceber'] = fluxo[periodo]['saldoReceber'] + receita.valor

    return fluxo

# recupera as seguintes informações do mês: saldo pago, saldo a pagar
def setResumoDespesas(fluxo):
    resultDespesas = Despesa.objects.all().order_by('-data_vencimento')
    for despesa in resultDespesas:
        if(despesa.data_pagamento):
            periodo = '%s/%s' % (despesa.data_pagamento.strftime("%m"), despesa.data_pagamento.strftime("%Y"))
        else:
            periodo = '%s/%s' % (despesa.data_vencimento.strftime("%m"), despesa.data_vencimento.strftime("%Y"))
        
        if(despesa.situacao == "PG"):
            fluxo[periodo]['saldoPago'] = fluxo[periodo]['saldoPago'] + despesa.valor
        else:
            fluxo[periodo]['saldoPagar'] = fluxo[periodo]['saldoPagar'] + despesa.valor

    return fluxo

# recupera as seguintes informações do mês: saldo inicial, saldo final, lucratividade, saldo previsto
def setSaldoIniFinLuc(fluxo, saldoInicial):
    setSaldoInicial = False
    saldoFinalMesAnterior = 0
    for periodo in reversed(fluxo):
        if(not setSaldoInicial):
            fluxo[periodo]['saldoInicial'] =  saldoInicial
            setSaldoInicial = True
        else:
            fluxo[periodo]['saldoInicial'] =  saldoFinalMesAnterior

        fluxo[periodo]['saldoFinal'] = fluxo[periodo]['saldoInicial'] + fluxo[periodo]['saldoRecebido'] - fluxo[periodo]['saldoPago']
        fluxo[periodo]['lucratividade'] = fluxo[periodo]['saldoFinal'] - fluxo[periodo]['saldoInicial']
        saldoFinalMesAnterior = fluxo[periodo]['saldoFinal']
        fluxo[periodo]['saldoPrevisto'] = fluxo[periodo]['saldoFinal'] + fluxo[periodo]['saldoReceber'] - fluxo[periodo]['saldoPagar']
    
    return fluxo

# coloca as receitas em ordem por classificação
def setReceitasOrder(fluxo):
    receitas = list(Receita.objects.all())
    receitas.sort(key=operator.methodcaller('get_classificacao_display'))
    for receita in receitas:
        periodo = '%s/%s' % (receita.data_expectativa.strftime("%m"), receita.data_expectativa.strftime("%Y"))
        dtExpectativa = '%s/%s/%s' % (receita.data_expectativa.strftime("%d"), receita.data_expectativa.strftime("%m"), receita.data_expectativa.strftime("%Y"))
        receita.data_expectativa = dtExpectativa
        if(receita.data_recebimento):
            periodo = '%s/%s' % (receita.data_recebimento.strftime("%m"), receita.data_recebimento.strftime("%Y"))
            dtrecebimento = '%s/%s/%s' % (receita.data_recebimento.strftime("%d"), receita.data_recebimento.strftime("%m"), receita.data_recebimento.strftime("%Y"))
            receita.data_recebimento = dtrecebimento

        fluxo[periodo]['receitas'].append(receita)

    return fluxo

# coloca as despesas em ordem por classificação
def setDespesasOrder(fluxo):
    despesas = list(Despesa.objects.all())
    despesas.sort(key=operator.methodcaller('get_classificacao_display'))
    for despesa in despesas:
        periodo = '%s/%s' % (despesa.data_vencimento.strftime("%m"), despesa.data_vencimento.strftime("%Y"))
        dtVencimento = '%s/%s/%s' % (despesa.data_vencimento.strftime("%d"), despesa.data_vencimento.strftime("%m"), despesa.data_vencimento.strftime("%Y"))
        despesa.data_vencimento = dtVencimento
        if(despesa.data_pagamento):
            periodo = '%s/%s' % (despesa.data_pagamento.strftime("%m"), despesa.data_pagamento.strftime("%Y"))
            dtpagamento = '%s/%s/%s' % (despesa.data_pagamento.strftime("%d"), despesa.data_pagamento.strftime("%m"), despesa.data_pagamento.strftime("%Y"))
            despesa.data_pagamento = dtpagamento
        
        fluxo[periodo]['despesas'].append(despesa)

    return fluxo

# adiciona para cada despesa paga e cada receita recebida, o saldo acumulado
def setSaldoAcumulado(fluxo, saldoInicial):
    valorAcumulado = saldoInicial
    for periodo in reversed(fluxo):
        for despesa in reversed(fluxo[periodo]['despesas']):
            if(despesa.situacao == "PG"):
                valorAcumulado = valorAcumulado - despesa.valor
                despesa.saldoAcumulado = valorAcumulado
        for receita in reversed(fluxo[periodo]['receitas']):
            if(receita.situacao == "PR"):
                valorAcumulado = valorAcumulado + receita.valor
                receita.saldoAcumulado = valorAcumulado

    return fluxo
