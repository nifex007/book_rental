from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Customer(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=225)
    # username = None

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

