from django.contrib import admin

from .models import Location, Visit, Route, Achievement,Comment,ForumPost,ForumCategory

admin.site.register(Location)
admin.site.register(Visit)
admin.site.register(Route)
admin.site.register(Achievement)
admin.site.register(Comment)
admin.site.register(ForumPost)
admin.site.register(ForumCategory)
