from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        related_name='subscribers',
        verbose_name='Избранное',
        blank=True,
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='cooking_chef',
        verbose_name='В списке покупок',
        blank=True,
    )
    followings = models.ManyToManyField(
        'users.UserModel',
        related_name='followers',
        verbose_name='Подписки',
        blank=True,
    )
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email',)
