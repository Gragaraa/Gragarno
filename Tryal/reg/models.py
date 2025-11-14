from django.db import models
from django.contrib.auth.models import AbstractUser
class myuser(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)

# Create your models here.
