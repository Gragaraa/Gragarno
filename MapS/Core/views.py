from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from .models import Location, Visit, Route
import requests


def index(request):
    return render(request, 'Core/index.html')


@login_required
def map_view(request):
    user_visits = Visit.objects.filter(user=request.user).select_related('location')
    return render(request, 'Core/map.html', {'user_visits': user_visits})


@login_required
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat, lon = data.get('lat'), data.get('lon')
            name = data.get('name', 'Новое место')

            # Геокодинг
            country, city = "Неизвестно", "Неизвестно"
            try:
                url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                headers = {'User-Agent': 'TravelMapApp/1.0'}
                res = requests.get(url, headers=headers, timeout=5).json()
                address = res.get('address', {})
                country = address.get('country', "Неизвестно")
                city = address.get('city', address.get('town', "Неизвестно"))
            except:
                pass

            loc = Location.objects.create(name=name, lat=lat, lon=lon, country=country, city=city)
            Visit.objects.create(user=request.user, location=loc)

            # Геймификация (НЕ ЗАВИСИТ ОТ УДАЛЕНИЯ ТОЧЕК)
            user = request.user
            user.total_points_ever += 1
            user.experience += 50

            if not user.ach_first_point:
                user.ach_first_point = True

            if user.total_points_ever >= 10 and not user.ach_country_explorer:
                user.ach_country_explorer = True
                user.title = "Опытный бродяга"

            if user.experience >= 500:
                user.level += 1
                user.experience = 0

            user.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def create_route(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Route.objects.create(
                user=request.user,
                name=data.get('name'),
                description=data.get('description', ''),
                points_json=data.get('points')
            )
            return JsonResponse({'status': 'success'})  # ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ТУТ
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)


@login_required
def delete_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id, user=request.user)
    visit.delete()
    return JsonResponse({'status': 'success'})


@login_required
def routes_list(request):
    routes = Route.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'Core/routes_list.html', {'routes': routes})


@login_required
def view_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    return render(request, 'Core/view_route.html', {'route': route})


@login_required
def achievements_view(request):
    # Теперь просто отдаем юзера, а в шаблоне смотрим его Boolean поля
    return render(request, 'Core/achievements.html')