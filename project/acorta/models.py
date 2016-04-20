from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Url(models.Model):
    url_corta = models.IntegerField()
    url_larga = models.CharField(max_length=128)
