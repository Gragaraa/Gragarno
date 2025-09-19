from django.db import models

from django.db import models


class Event(models.Model):
    data = models.CharField(max_length=120)
    description = models.TextField(max_length=500)