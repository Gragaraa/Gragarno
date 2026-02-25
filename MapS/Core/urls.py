"""
URL configuration for MapS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path('map/', views.map_view,name='map_page'),
    path('save_location/', views.save_location,name='save_location'),
    path('create-route/', views.create_route, name='create_route'),
    path('delete-visit/<int:visit_id>/', views.delete_visit, name='delete_visit'),
    path('my-routes/', views.routes_list, name='routes_list'),
    path('route/<int:route_id>/', views.view_route, name='view_route'),
    path('achievements/',views.achievements_view,name='achievements'),
    path('game', views.geoguessr_game,name='geoguessr'),
    path('game/submit/', views.submit_guess,name='submit_guess')

]
