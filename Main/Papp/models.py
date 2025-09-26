from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class Event(models.Model):
    data = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
class User(AbstractUser):
    pass