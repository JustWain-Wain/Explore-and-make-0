from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=128, blank=True)
    position = models.CharField(max_length=128, blank=True)
