from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                           ShoppingCartView, TagViewSet,
                           download_shopping_cart)
from users.views import FollowCreateDestroyView, FollowListView

router = DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart',
    ),
    path('', include(router.urls)),
    path(
        'users/subscriptions/',
        FollowListView.as_view(),
        name='subscriptions',
    ),
    path(
        'users/<int:user_id>/subscribe/',
        FollowCreateDestroyView.as_view(),
        name='subscribe'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteView.as_view(),
        name='favorite',
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping_cart',
    ),
]
