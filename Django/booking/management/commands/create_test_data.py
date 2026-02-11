from django.core.management.base import BaseCommand
from booking.models import Room

class Command(BaseCommand):
    help = 'Создаёт тестовые комнаты'

    def handle(self, *args, **kwargs):
        Room.objects.create(name="Переговорная А", capacity=10, has_projector=True)
        Room.objects.create(name="Переговорная Б", capacity=6, has_projector=False)
        Room.objects.create(name="Большой зал", capacity=50, has_projector=True)
        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы'))