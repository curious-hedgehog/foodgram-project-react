from django.contrib.auth import get_user_model
from django.db import models

from recipes.constants import LONG_FIELD_MAX_LENGTH, SHORT_FIELD_MAX_LENGTH
from recipes.validators import validate_positive

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=LONG_FIELD_MAX_LENGTH, verbose_name='Название'
    )
    color = models.CharField(
        max_length=SHORT_FIELD_MAX_LENGTH, verbose_name='Цветовой код'
    )
    slug = models.SlugField(
        max_length=SHORT_FIELD_MAX_LENGTH, verbose_name='Slug', unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=LONG_FIELD_MAX_LENGTH, verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=SHORT_FIELD_MAX_LENGTH, verbose_name='Единица измерения'
    )

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    name = models.CharField(
        max_length=LONG_FIELD_MAX_LENGTH, verbose_name='Название'
    )
    image = models.ImageField(verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления', validators=(validate_positive,)
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='ingredients', on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name='recipes', on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Количество', validators=(validate_positive,)
    )

    class Meta:
        verbose_name = 'Ингредиент к рецепту'
        verbose_name_plural = 'Ингредиенты к рецепту'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredients for recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'
