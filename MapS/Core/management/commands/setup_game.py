from django.core.management.base import BaseCommand
from Core.models import Location


from Core.models import Location
import os


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        locations = [
            {"name": "Париж", "lat": 48.8584, "lon": 2.2945, "file": "panoramas/paris.jpg"},
            {"name": "Москва", "lat": 55.7539, "lon": 37.6208, "file": "panoramas/moscow.jpg"},
        ]

        for loc in locations:
            Location.objects.get_or_create(
                name=loc['name'],
                defaults={
                    'lat': loc['lat'],
                    'lon': loc['lon'],
                    'is_game_task': True,
                    'panorama_file': loc['file']
                }
            )
        self.stdout.write("Локации обновлены!")