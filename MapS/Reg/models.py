from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, verbose_name="О себе")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    level = models.PositiveIntegerField(default=1, verbose_name="Уровень")
    experience = models.PositiveIntegerField(default=0, verbose_name="Опыт")
    title = models.CharField(max_length=100, default="Исследователь", verbose_name="Звание")
    total_experience = models.PositiveIntegerField(default=0, verbose_name="Опыт")

    ach_1_point = models.BooleanField(default=False)
    ach_10_points = models.BooleanField(default=False)
    ach_50_points = models.BooleanField(default=False)

    ach_3_countries = models.BooleanField(default=False)
    ach_1_route = models.BooleanField(default=False)
    ach_5_routes = models.BooleanField(default=False)
    total_points_ever = models.IntegerField(default=0)
    total_routes_ever=models.IntegerField(default=0)

    def __str__(self):
        return self.username

    @property
    def xp_to_next_level(self):
        return self.level * 500

    def add_xp(self, amount):
        self.experience += amount

        while self.experience >= self.xp_to_next_level:
            self.experience -= self.xp_to_next_level
            self.level += 1
            if self.level == 5: self.title = "Странник"
            if self.level == 10: self.title = "Первопроходец"
            if self.level == 20: self.title = "Магистр Карты"
        self.save()