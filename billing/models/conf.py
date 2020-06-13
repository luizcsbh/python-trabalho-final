from django.db import models

class Conf(models.Model):
    saldoInicial = models.DecimalField(null=True, max_digits=8, decimal_places=2)