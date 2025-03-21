from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

class trains(models.Model):
    trainname=models.CharField(default=" ",max_length=100)
    trainnumber=models.CharField(default=0,max_length=100)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    date=models.DateField(default=timezone.now)
    time=models.TimeField(default=timezone.now)
    seats=models.CharField(default=100,max_length=100)
    price=models.CharField(max_length=100)
    
def __str__(self):
    return self.trainname 

class Books(models.Model):
    trainnumber=models.CharField(default=0,max_length=100)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    personname=models.CharField(default=" ",max_length=100)
    email=models.EmailField(default=" ",max_length=254)
    age=models.CharField(default=0,max_length=100)
    gender=models.CharField(default=" ",max_length=100)
def __str__(self):
    return self.trainnumber

class payment(models.Model):
    status=models.CharField(default=" ",max_length=100)
    amount=models.CharField(default=" ",max_length=100)
def __str__(self):
    return self.status

