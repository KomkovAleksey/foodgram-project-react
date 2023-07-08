import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Команда для импорта данных из файла csv в базу данных:
    python manage.py import_ingredients_data
    команда в докер контейнере:
    docker compose exec backend python manage.py import_ingredients_data
    """

    help = "Заполняем базу данных ингридиентов."

    def handle(self, **kwargs):
        with open(
                './data/ingredients.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        self.stdout.write(
            self.style.SUCCESS("[+]***Данные ингридиентов загружены!***")
        )
