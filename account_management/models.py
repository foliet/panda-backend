from django.db import models
from django.contrib.auth.models import User as User1
import re


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    learner_level = models.CharField(max_length=10)
    points = models.IntegerField()
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    portrait_url = models.CharField(max_length=200)
