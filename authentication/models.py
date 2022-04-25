from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    learner_level = models.CharField(max_length=10)
    points = models.IntegerField()
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    avatar_url = models.CharField(max_length=200)
