from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    inn = models.CharField(max_length=9, null=False)
    cash = models.DecimalField(max_digits=20, default=0, decimal_places=2, null=False)
