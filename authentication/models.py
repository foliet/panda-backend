from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("learner_level", "0")
        extra_fields.setdefault("point", 0)
        extra_fields.setdefault("country", "")
        extra_fields.setdefault("age", 0)
        extra_fields.setdefault("avatar_url", "http://1.117.107.95/img/portrait.f98bd381.svg")
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("learner_level", "0")
        extra_fields.setdefault("points", 0)
        extra_fields.setdefault("country", "")
        extra_fields.setdefault("age", 0)
        extra_fields.setdefault("avatar_url", "http://1.117.107.95/img/portrait.f98bd381.svg")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    learner_level = models.CharField(max_length=10)
    points = models.IntegerField()
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    avatar_url = models.CharField(max_length=200)

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
