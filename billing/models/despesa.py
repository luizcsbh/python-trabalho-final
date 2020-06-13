from django.db import models

class Despesa(models.Model):
    CLASSIFICACAO_CHOICES = (
        ('AG', 'Água'),
        ('AL', 'Alimentação'),
        ('AG', 'Aluguel'),
        ('EN', 'Energia'),
        ('LA', 'Lazer'),
        ('OU', 'Outros'),
        ('TE', 'Telecomunicações'),
        ('TR', 'Transporte')
    )

    FORMA_PAGAMENTO_CHOICES = (
        ('B', 'Boleto'),
        ('C', 'Crédito'),
        ('D', 'Débito'),
        ('M', 'Dinheiro'),
        ('P', 'Depósito'),
        ('O', 'Outros')
    )
    
    SITUACAO_CHOICES = (
        ('PG', 'Pago'),
        ('AP', 'A pagar')
    )
    
    classificacao = models.CharField(max_length=2, choices=CLASSIFICACAO_CHOICES, default='OU')
    data_pagamento = models.DateField(null=True)
    data_vencimento = models.DateField(null=False)
    descricao = models.CharField(max_length=255)
    formaPagamento = models.CharField(max_length=1, choices=FORMA_PAGAMENTO_CHOICES, default='O')
    situacao = models.CharField(max_length=2, choices=SITUACAO_CHOICES, default='AP')
    valor = models.DecimalField(null=False, max_digits=8, decimal_places=2)
    