from django.db import models
class Forum(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()