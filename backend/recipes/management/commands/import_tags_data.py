import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """
    Команда для импорта данных из файла csv в базу данных:
    python manage.py import_tags_data
    команда в докер контейнере:
    docker compose exec backend python manage.py import_tags_data
    """

    help = "Заполняем базу данных тегов."

    def handle(self, **kwargs):
        with open(
                './data/tags.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                name, color, slug = row
                Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug
                )
        self.stdout.write(
            self.style.SUCCESS("[+]***Данные тегов загружены!***")
        )
