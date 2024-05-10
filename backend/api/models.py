from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from api.constants import NAME_MAX_LENGTH, COLOR_MAX_LENGTH, UNIT_MAX_LENGTH

from api.constants import SLUG_MAX_LENGTH

User = get_user_model()


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s не является положительным числом"),
            params={"value": value},
        )


class Tag(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название'
    )
    color = models.CharField(verbose_name='Цветовой код', max_length=COLOR_MAX_LENGTH)
    slug = models.SlugField(unique=True, max_length=SLUG_MAX_LENGTH,
                            verbose_name='Slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(
        max_length=UNIT_MAX_LENGTH, verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название'
    )
    measurement_unit = models.CharField(max_length=UNIT_MAX_LENGTH,
                             verbose_name='Единица измерения')

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    name = models.CharField(
        max_length=NAME_MAX_LENGTH, verbose_name='Название'
    )
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=[validate_positive]
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='ingredients', on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name='recipes', on_delete=models.CASCADE
    )
    amount = models.IntegerField(verbose_name='Количество', validators=[validate_positive])

    class Meta:
        verbose_name = 'Пара "Рецепт - ингредиент"'
        verbose_name_plural = 'Пары "Рецепт - ингредиент"'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredients for recipe'
        )]
