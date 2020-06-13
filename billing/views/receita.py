from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from ..models import Receita

# GET: abre uma página para criar uma receita
# POST: cria no banco uma nova receita baseado nos dados do form
@require_http_methods(["GET", "POST"])    
@csrf_exempt
def receita(request):
    if(request.method=="GET"):
        context = criaContextNovaReceita()
        return render(request, 'receita.html', context)
    elif(request.method=="POST"):
        salvaNovaReceita(request)
        context = criaContextNovaReceita()
        context["message"] = 'Receita cadastrada com sucesso!'
        return render(request, 'receita.html', context)
       

# GET: abre uma página para editar a receita de ID = id_receita
# POST: atualiza no banco a receita de ID = id_receita baseado nos dados do form
# DELETE: deleta do banco a receita de ID = id_receita, e retorna um JSON
@require_http_methods(["GET", "POST", "DELETE"])    
@csrf_exempt
def receitaOp(request, id_receita):
    receita = None
    try:
        receita = Receita.objects.get(id=id_receita)
    except ObjectDoesNotExist:
        print(f"""Receita não existe!""")

    if(request.method=="GET"):
        context = {}
        if(receita):
            dtExpectativa = '%s-%s-%s' % (receita.data_expectativa.strftime("%Y"), receita.data_expectativa.strftime("%m"), receita.data_expectativa.strftime("%d"))
            receita.data_expectativa = dtExpectativa
            if(receita.data_recebimento):
                dtrecebimento = '%s-%s-%s' % (receita.data_recebimento.strftime("%Y"), receita.data_recebimento.strftime("%m"), receita.data_recebimento.strftime("%d"))
                receita.data_recebimento = dtrecebimento
            
            context = initContextReceita(receita)

        return render(request, 'receita.html', context)
    elif(request.method=="POST"):
        context = criaContextNovaReceita()
        if(receita):
            atualizaReceita(request, id_receita)
            context["message"] = 'Receita atualizada com sucesso!'
            
        return render(request, 'receita.html', context)
    elif(request.method=="DELETE"):
        jsonReturn = {"success" : False}
        if(receita):
            receita.delete()
            jsonReturn = {"success" : True}
        
        return JsonResponse(jsonReturn)

# inicializa o context vazio
def initContextReceita(receita):
    context = { 
        'receita' : receita,
        'classificacoes' : [],
        'formasRecebimento' : [],
        'situacoes' : []
    }
    
    fieldsClassificacao = Receita.CLASSIFICACAO_CHOICES
    for field, value in fieldsClassificacao:
        itemClassificacao = {"key" : field, "value" : value}
        context["classificacoes"].append(itemClassificacao)

    fieldsFormasRecebimento = Receita.FORMA_RECEBIMENTO_CHOICES
    for field, value in fieldsFormasRecebimento:
        itemFormaRecebimento = {"key" : field, "value" : value}
        context["formasRecebimento"].append(itemFormaRecebimento)

    fieldsSituacoes = Receita.SITUACAO_CHOICES
    for field, value in fieldsSituacoes:
        itemSituacao = {"key" : field, "value" : value}
        context["situacoes"].append(itemSituacao)
    
    return context

# cria o context para exibir na página de nova receita
def criaContextNovaReceita():
    dtToday = '%s-%s-%s' % (date.today().strftime("%Y"), date.today().strftime("%m"), date.today().strftime("%d"))
    receita = Receita(classificacao='OU',
                    data_expectativa=dtToday,
                    data_recebimento='',
                    descricao='',
                    formaRecebimento='O',
                    situacao='AR',
                    valor=''
                )

    context = initContextReceita(receita)
    return context

# salva as informações da nova receita
def salvaNovaReceita(request):
    valor = request.POST['valor']

    dataRecebimento = request.POST['data_recebimento']
    if(dataRecebimento == ""):
        dataRecebimento = None

    receita = Receita(classificacao=request.POST['classificacao'],
                    data_expectativa=request.POST['data_expectativa'],
                    data_recebimento=dataRecebimento,
                    descricao=request.POST['descricao'],
                    formaRecebimento=request.POST['formaRecebimento'],
                    situacao=request.POST['situacao'],
                    valor=valor
                    )

    receita.save()

# atualiza as informações de uma receita existente
def atualizaReceita(request, id_receita):
    valor = request.POST['valor']

    dataRecebimento = request.POST['data_recebimento']
    if(dataRecebimento == ""):
        dataRecebimento = None

    receita = Receita(id=id_receita,
                    classificacao=request.POST['classificacao'],
                    data_expectativa=request.POST['data_expectativa'],
                    data_recebimento=dataRecebimento,
                    descricao=request.POST['descricao'],
                    formaRecebimento=request.POST['formaRecebimento'],
                    situacao=request.POST['situacao'],
                    valor=valor
                    )

    receita.save()
