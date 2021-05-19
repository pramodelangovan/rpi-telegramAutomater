from django.db import models


class goldRates(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=256)
    oneGramRate = models.CharField(max_length=256)
    soverignRate = models.CharField(max_length=256)
    tenGramRate = models.CharField(max_length=256)
    differencePerGram = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    purity = models.CharField(max_length=256)
    city = models.CharField(max_length=256)

class users(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=512)
    name = models.CharField(max_length=512, default="")
    isAdmin = models.BooleanField(default=False)
    addedBy = models.CharField(max_length=512)
    addedOn = models.DateTimeField(auto_now_add=True)