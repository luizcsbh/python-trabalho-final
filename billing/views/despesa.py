from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ..models import Despesa

# GET: abre uma página para criar uma despesa
# POST: cria no banco uma nova despesa baseado nos dados do form
@require_http_methods(["GET", "POST"])   
@csrf_exempt
def despesa(request):
    if(request.method=="GET"):
        context = criaContextNovaDespesa()
        return render(request, 'despesa.html', context)
    elif(request.method=="POST"):
        salvaNovaDespesa(request)
        context = criaContextNovaDespesa()
        context["message"] = 'Despesa cadastrada com sucesso!'
        return render(request, 'despesa.html', context)


# GET: abre uma página para editar a despesa de ID = id_despesa
# POST: atualiza no banco a despesa de ID = id_despesa baseado nos dados do form
# DELETE: deleta do banco a despesa de ID = id_despesa, e retorna um JSON
@require_http_methods(["GET", "POST", "DELETE"])  
@csrf_exempt
def despesaOp(request, id_despesa):
    despesa = None
    try:
        despesa = Despesa.objects.get(id=id_despesa)
    except ObjectDoesNotExist:
        print(f"""Despesa não existe!""")

    if(request.method=="GET"):
        context = {}
        if(despesa):
            dtVencimento = '%s-%s-%s' % (despesa.data_vencimento.strftime("%Y"), despesa.data_vencimento.strftime("%m"), despesa.data_vencimento.strftime("%d"))
            despesa.data_vencimento = dtVencimento
            if(despesa.data_pagamento):
                dtPagamento = '%s-%s-%s' % (despesa.data_pagamento.strftime("%Y"), despesa.data_pagamento.strftime("%m"), despesa.data_pagamento.strftime("%d"))
                despesa.data_pagamento = dtPagamento
            
            context = initContextDespesa(despesa)

        return render(request, 'despesa.html', context)
    elif(request.method=="POST"):
        context = criaContextNovaDespesa()
        if(despesa):
            atualizaDespesa(request, id_despesa)
            context["message"] = 'Despesa atualizada com sucesso!'
            
        return render(request, 'despesa.html', context)
    elif(request.method=="DELETE"):
        jsonReturn = {"success" : False}
        if(despesa):
            despesa.delete()
            jsonReturn = {"success" : True}
        
        return JsonResponse(jsonReturn)

# inicializa o context vazio
def initContextDespesa(despesa):
    context = { 
        'despesa' : despesa,
        'classificacoes' : [],
        'formasPagamento' : [],
        'situacoes' : []
    }
    
    fieldsClassificacao = Despesa.CLASSIFICACAO_CHOICES
    for field, value in fieldsClassificacao:
        itemClassificacao = {"key" : field, "value" : value}
        context["classificacoes"].append(itemClassificacao)

    fieldsFormasPagamento = Despesa.FORMA_PAGAMENTO_CHOICES
    for field, value in fieldsFormasPagamento:
        itemFormaPagamento = {"key" : field, "value" : value}
        context["formasPagamento"].append(itemFormaPagamento)

    fieldsSituacoes = Despesa.SITUACAO_CHOICES
    for field, value in fieldsSituacoes:
        itemSituacao = {"key" : field, "value" : value}
        context["situacoes"].append(itemSituacao)
    
    return context

# cria o context para exibir na página de nova despesa
def criaContextNovaDespesa():
    dtToday = '%s-%s-%s' % (date.today().strftime("%Y"), date.today().strftime("%m"), date.today().strftime("%d"))
    despesa = Despesa(classificacao='OU',
                      data_pagamento='',
                      data_vencimento=dtToday,
                      descricao='',
                      formaPagamento='O',
                      situacao='AP',
                      valor=''
                    )
    context = initContextDespesa(despesa)
    return context

# salva as informações da nova despesa
def salvaNovaDespesa(request):
    valor = request.POST['valor']

    dataPagamento = request.POST['data_pagamento']
    if(dataPagamento == ""):
        dataPagamento = None

    despesa = Despesa(classificacao=request.POST['classificacao'],
                      data_pagamento=dataPagamento,
                      data_vencimento=request.POST['data_vencimento'],
                      descricao=request.POST['descricao'],
                      formaPagamento=request.POST['formaPagamento'],
                      situacao=request.POST['situacao'],
                      valor=valor
                    )

    despesa.save()

# atualiza as informações de uma despesa existente
def atualizaDespesa(request, id_despesa):
    valor = request.POST['valor']

    dataPagamento = request.POST['data_pagamento']
    if(dataPagamento == ""):
        dataPagamento = None

    despesa = Despesa(id=id_despesa,
                      classificacao=request.POST['classificacao'],
                      data_pagamento=dataPagamento,
                      data_vencimento=request.POST['data_vencimento'],
                      descricao=request.POST['descricao'],
                      formaPagamento=request.POST['formaPagamento'],
                      situacao=request.POST['situacao'],
                      valor=valor
                    )

    despesa.save()
