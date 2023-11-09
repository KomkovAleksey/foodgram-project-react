"""
Custom django-admin command to load data from csv files.
"""
import os
import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Command to import data from csv file into databases:
    python Manage.py import_ingredients_data
    in a docker container:
    docker compose exec backend python manage.py import_ingredients_data
    """

    help = 'Filling out the ingredients database.'

    def handle(self, **kwargs):
        starting_message = (
            '***Starting filling out the ingredients database!!!***'
        )
        self.stdout.write(self.style.WARNING(f'{starting_message}'))
        ingredients_file_path = './data/ingredients.csv'
        if os.path.exists(ingredients_file_path):
            with open(ingredients_file_path, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
            self.stdout.write(
                self.style.SUCCESS('***Ingredient data loaded!***')
            )
        else:
            self.stdout.write(
                self.style.ERROR('***File ingredients.csv not found!***')
            )
