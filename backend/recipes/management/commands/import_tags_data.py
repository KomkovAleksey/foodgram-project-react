"""
Custom django-admin command to load data from csv files.
"""
import os
import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    """
    Command to import data from csv file into database:
    python manage.py import_tags_data
    command in docker container:
    docker compose exec backend python manage.py import_tags_data
    """

    help = 'Filling out the tag database.'

    def handle(self, **kwargs):
        starting_message = '***Starting filling out the tag database!!!***'
        self.stdout.write(self.style.WARNING(f'{starting_message}'))
        tags_file_path = './data/tags.csv'
        if os.path.exists(tags_file_path):
            with open(tags_file_path, encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    name, color, slug = row
                    Tag.objects.get_or_create(
                        name=name,
                        color=color,
                        slug=slug
                    )
            self.stdout.write(self.style.SUCCESS('***Tag data loaded!***'))
        else:
            self.stdout.write(self.style.ERROR('***File tags.csv not found!***'))
