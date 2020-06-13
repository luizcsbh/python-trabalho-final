from django.urls import path

from .views import index as iv
from .views import despesa as dv
from .views import receita as rv
from .views import relatorio as relv

urlpatterns = [
    path('', iv.index, name="index"),

    path('despesa/', dv.despesa, name="despesa"),
    path('despesa/<int:id_despesa>/', dv.despesaOp, name="despesaOp"),

    path('receita/', rv.receita, name="receita"),
    path('receita/<int:id_receita>/', rv.receitaOp, name="receitaOp"),

    path('relatorio/despesas', relv.despesas, name="relatorio_despesas"),
    path('relatorio/despesas/filtro', relv.despesasFiltro, name="relatorio_despesas_filtro"),
    path('relatorio/receitas', relv.receitas, name="relatorio_receitas"),
    path('relatorio/receitas/filtro', relv.receitasFiltro, name="relatorio_receitas_filtro")
]