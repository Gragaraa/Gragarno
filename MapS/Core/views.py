from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from .models import Location, Visit, Route
def index(request):
    return render(request,'Core/index.html')


@login_required
def map_view(request):
    # Загружаем все посещения текущего юзера, чтобы отобразить их при входе
    user_visits = Visit.objects.filter(user=request.user).select_related('location')
    return render(request, 'Core/map.html', {'user_visits': user_visits})





@login_required
def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat')
        lon = data.get('lon')
        name = data.get('name', 'Новое место')


        loc = Location.objects.create(
            name=name,
            country="Неизвестно",
            lat=lat,
            lon=lon
        )


        Visit.objects.create(
            user=request.user,
            location=loc
        )

        return JsonResponse({'status': 'success', 'message': 'Точка сохранена!'})

    return JsonResponse({'status': 'error'}, status=400)



@login_required
def create_route(request):
    from .models import Route
    if request.method == 'POST':
        data = json.loads(request.body)
        visit_ids = data.get('visit_ids') # Список ID точек
        route_name = data.get('name')
        route_desc = data.get('description')

        route = Route.objects.create(user=request.user, name=route_name, description=route_desc)
        route.visits.set(visit_ids) # Привязываем точки к маршруту
        return JsonResponse({'status': 'success'})

@login_required
def delete_visit(request, visit_id):
    visit = Visit.objects.get(id=visit_id, user=request.user)
    visit.delete()
    return JsonResponse({'status': 'success'})