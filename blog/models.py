from django.db import models

# Create your models here.


class Article(models.Model):
    adate = models.DateTimeField(auto_now=True)
    alast_revise = models.DateTimeField(auto_now_add=True, null=True)
    atitle = models.CharField(max_length=128)
    acontent = models.TextField()
    aview = models.IntegerField(default=0)
    aclass = models.IntegerField(default=0)


class Account(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

