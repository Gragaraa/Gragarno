from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    level = models.PositiveIntegerField(default=1, verbose_name="Уровень")
    experience = models.PositiveIntegerField(default=0, verbose_name="Опыт")
    title = models.CharField(max_length=100, default="Исследователь", verbose_name="Звание")
    ach_first_point = models.BooleanField(default=False)
    ach_country_explorer = models.BooleanField(default=False)
    ach_master_of_routes = models.BooleanField(default=False)
    total_points_ever = models.IntegerField(default=0)

    def __str__(self):
        return self.username

