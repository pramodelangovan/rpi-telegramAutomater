from django.db import models


class goldRates(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=256)
    oneGramRate = models.CharField(max_length=256)
    soverignRate = models.CharField(max_length=256)
    tenGramRate = models.CharField(max_length=256)
    difference = models.CharField(max_length=256)
    state = models.CharField(max_length=256)