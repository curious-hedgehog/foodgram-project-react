from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    favorites = models.ManyToManyField(
        'api.Recipe', related_name='subscriber',
        verbose_name='Избранное', blank=True
    )
    shopping_cart = models.ManyToManyField(
        'api.Recipe', related_name='cooking_chef',
        verbose_name='В списке покупок', blank=True
    )
    followings = models.ManyToManyField(
        'users.UserModel', related_name='followers',
        verbose_name='Подписки', blank=True
    )
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


# class Follow(models.Model):
#     user = models.ForeignKey(
#         UserModel, on_delete=models.CASCADE, related_name='followings'
#     )
#     following = models.ForeignKey(
#         UserModel, on_delete=models.CASCADE, related_name='followers'
#     )
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'following'],
#                 name='unique_following_record'
#             )
#         ]