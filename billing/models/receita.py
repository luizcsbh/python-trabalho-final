from django.db import models

class Receita(models.Model):
    CLASSIFICACAO_CHOICES = (
        ('DT', 'Dívida de terceiros'),
        ('DO', 'Doação'),
        ('SA', 'Salário'),
        ('SP', 'Serviço prestado'),
        ('OU', 'Outros'),
        ('VE', 'Vendas')
    )

    FORMA_RECEBIMENTO_CHOICES = (
        ('B', 'Boleto'),
        ('C', 'Crédito'),
        ('D', 'Débito'),
        ('M', 'Dinheiro'),
        ('P', 'Depósito'),
        ('O', 'Outros')
    )
    
    SITUACAO_CHOICES = (
        ('PR', 'Recebido'),
        ('AR', 'A receber')
    )
    
    classificacao = models.CharField(max_length=2, choices=CLASSIFICACAO_CHOICES, default='OU')
    data_expectativa = models.DateField(null=False)
    data_recebimento = models.DateField(null=True)
    descricao = models.CharField(max_length=255)
    formaRecebimento = models.CharField(max_length=1, choices=FORMA_RECEBIMENTO_CHOICES, default='O')
    situacao = models.CharField(max_length=2, choices=SITUACAO_CHOICES, default='AR')
    valor = models.DecimalField(null=False, max_digits=8, decimal_places=2)
    