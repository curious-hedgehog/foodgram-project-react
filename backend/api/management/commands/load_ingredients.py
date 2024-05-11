import csv
import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.models import Ingredient


class Command(BaseCommand):
    help = 'Imports ingredients from data/ingredients.csv to the database'

    def handle(self, *args, **options):
        file = settings.BASE_DIR / 'data/ingredients.csv'
        if not os.path.isfile(file):
            raise CommandError(f"Отсутствует файл: {file}")
        objects = []
        skipped_ingredients = 0
        with open(file, encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            if len(csv_reader.fieldnames) != 2 or any(
                    field not in csv_reader.fieldnames
                    for field in ['name', 'measurement_unit']
            ):
                raise CommandError(
                    'csv файл должен содержать две колонки: '
                    '"name" и "measurement_unit"'
                )
            for row in csv_reader:
                row = {key.lower(): value.lower() for key, value in row.items()}
                if Ingredient.objects.filter(**row).exists():
                    skipped_ingredients += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f'Ингредиент {row} уже существует в базе данных.'
                        )
                    )
                else:
                    objects.append(Ingredient(**row))
        Ingredient.objects.bulk_create(objects)
        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт закончен.\n'
                f'Загружено ингредиентов: {len(objects)}\n'
                f'Пропущено ингредиентов: {skipped_ingredients}'
            )
        )
