from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from .forms import CommentForm
from django.http import JsonResponse
from .models import Location, Visit, Route
import requests
import random
from math import radians, cos, sin, asin, sqrt
from .models import ForumCategory, ForumPost, Comment
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from django.shortcuts import redirect
from .models import Visit
User = get_user_model()
def get_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dLat, dLon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
    return R * 2 * asin(sqrt(a))
def index(request):

    top_users = User.objects.all().order_by('-total_experience')[:10]
    return render(request, 'Core/index.html', {'top_users': top_users})


@login_required
def map_view(request):

    user_visits = Visit.objects.filter(
        user=request.user
    ).exclude(
        location__name__icontains="Guess"
    ).exclude(
        location__is_game_task=True
    ).select_related('location')

    return render(request, 'Core/map.html', {'user_visits': user_visits})


@login_required
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lat, lon = data.get('lat'), data.get('lon')
            name = data.get('name', 'Новое место')


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


            user = request.user
            user.total_points_ever += 1
            xp = 100
            if not user.ach_1_point:
                user.ach_1_point = True
                xp += 100

            if user.total_points_ever >= 10 and not user.ach_10_points:
                user.ach_10_points = True
                xp += 500

            if user.total_points_ever >= 50 and not user.ach_50_points:
                user.ach_50_points = True
                xp += 2000
            if user.total_points_ever >= 500:
                xp += 400

            unique_countries = Visit.objects.filter(user=user).values('location__country').distinct().count()
            if unique_countries >= 3 and not user.ach_3_countries:
                user.ach_3_countries = True
                xp += 1500
            user.total_experience += xp
            user.add_xp(xp)
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

            user = request.user
            user.total_routes_ever += 1

            xp = 100

            routes_count = user.total_routes_ever
            if routes_count == 1 and not user.ach_1_route:
                user.ach_1_route = True
                xp += 300

            if routes_count >= 5 and not user.ach_5_routes:
                user.ach_5_routes = True
                xp += 1000
            if routes_count>=30:
                xp+=400
            user.total_experience+=xp
            user.add_xp(xp)
            return JsonResponse({'status': 'success'})
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

    return render(request, 'Core/achievements.html')

@login_required
def geoguessr_game(request):
    tasks = Location.objects.filter(is_game_task=True)
    if not tasks:
        return render(request, 'Core/game.html', {'error': 'Нет доступных панорам'})

    target = random.choice(tasks)

    past_guesses = Visit.objects.filter(user=request.user, location__name__icontains="Guess")

    return render(request, 'Core/game.html', {
        'target': target,
        'past_guesses': past_guesses,
        'api_key': settings.YANDEX_MAPS_API_KEY
    })


@login_required
def submit_guess(request):
    try:
        data = json.loads(request.body)
        target = get_object_or_404(Location, id=data['target_id'])

        dist = get_distance(target.lat, target.lon, data['lat'], data['lon'])


        xp = max(0, int(1000 - (dist * 2)))


        new_loc = Location.objects.create(
            name=f"Guess_{target.name}",
            lat=data['lat'],
            lon=data['lon'],
            is_game_task=False
        )
        Visit.objects.create(user=request.user, location=new_loc)


        user = request.user
        user.total_points_ever += 1
        user.add_xp(xp)


        if user.total_points_ever >= 10 and not user.ach_10_points:
            user.ach_10_points = True
            user.add_xp(500)

        user.save()

        return JsonResponse({
            'dist': round(dist, 1),
            'xp': xp,
            't_lat': target.lat,
            't_lon': target.lon
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



def forum_index(request):
    categories = ForumCategory.objects.all()
    return render(request, 'Core/forum/index.html', {'categories': categories})


def category_detail(request, pk):
    category = get_object_or_404(ForumCategory, pk=pk)
    sort = request.GET.get('sort', 'new')

    posts = category.posts.all()

    if sort == 'popular':

        posts = posts.annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
    else:
        posts = posts.order_by('-created_at')

    return render(request, 'Core/forum/category.html', {'category': category, 'posts': posts, 'current_sort': sort})


def user_list(request):
    users = User.objects.all().order_by('-level') # Топ по уровню
    return render(request, 'Core/user_list.html', {'users': users})


@login_required
def create_post(request, category_id):
    category = get_object_or_404(ForumCategory, id=category_id)

    if category.is_readonly and not request.user.is_staff:
        messages.error(request, "Писать сюда могут только админы!")
        return redirect('category_detail', pk=category.id)

    # ПРОВЕРКА КУЛДАУНА
    last_post = ForumPost.objects.filter(author=request.user).order_by('-created_at').first()
    if last_post:
        diff = (timezone.now() - last_post.created_at).total_seconds()
        if diff < 300:  # 5 минут = 300 секунд
            wait = int(300 - diff)
            messages.error(request, f"Подожди еще {wait} сек. перед созданием нового поста!")
            return redirect('category_detail', pk=category.id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.category = category
            post.save()
            return redirect('category_detail', pk=category.id)
    else:
        form = PostForm()
    return render(request, 'Core/forum/create_post.html', {'form': form, 'category': category})


def post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    sort = request.GET.get('sort', 'old')

    if sort == 'new':
        comments = post.comments.all().order_by('-created_at')
    else:
        comments = post.comments.all().order_by('created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated: return redirect('login')


        last_comment = Comment.objects.filter(author=request.user).order_by('-created_at').first()
        if last_comment:
            if (timezone.now() - last_comment.created_at).total_seconds() < 30:
                messages.error(request, "Не части! Комменты раз в 30 секунд.")
                return redirect('post_detail', post_id=post.id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'Core/forum/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'current_sort': sort})
@login_required
def vote_post(request, post_id, action):
    post = get_object_or_404(ForumPost, id=post_id)
    if action == 'like':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            post.dislikes.remove(request.user)
    elif action == 'dislike':
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
            post.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'forum_index'))




@login_required
def clear_history(request):
    if request.user.is_authenticated:
        Visit.objects.filter(user=request.user).delete()
    guess_locations = Location.objects.filter(name__icontains="Guess")
    guess_locations.delete()

    return redirect('geoguessr')


