from django.db import models
from django.conf import settings



class Location(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    lon= models.FloatField(verbose_name="Долгота",default=0.0)
    lat=models.FloatField(verbose_name="Широта", default=0.0)
    city=models.CharField(max_length=100, blank=True, null=True)
    is_game_task = models.BooleanField(default=False, verbose_name="Это точка-задание для игры")
    panorama_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на панораму 360")
    panorama_file= models.ImageField(upload_to='panoramas/',blank=True,null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return f"{self.name}, {self.country}"


class Visit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visits')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_visited = models.DateField(auto_now_add=True, verbose_name="Дата посещения")
    notes = models.TextField(blank=True, verbose_name="Заметки из путешествия")


class Route(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Название маршрута")
    description = models.TextField(blank=True)
    points_json = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


class Achievement(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название достижения")
    description = models.TextField(verbose_name="Условие получения")
    icon = models.ImageField(upload_to='achievements/', null=True, blank=True)

class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_unlocked = models.DateTimeField(auto_now_add=True)
class ForumCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название раздела")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, default="💬", verbose_name="Эмодзи-иконка")
    is_readonly = models.BooleanField(default=False, verbose_name='Только для админов')

    def __str__(self):
        return f"{self.icon} {self.name}"

class ForumPost(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='posts', null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст поста")
    image = models.ImageField(upload_to='forum_pics/', null=True, blank=True, verbose_name="Картинка")
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_dislikes', blank=True)

    def total_score(self):
        return self.likes.count() - self.dislikes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




