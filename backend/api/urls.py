from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet, FavoriteCreateDestroyView, \
    ShoppingCartCreateDestroyView, download_shopping_cart
from users.views import UserViewSet, FollowListView, FollowCreateDestroyView

router = DefaultRouter()
# router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart',
    ),
    path('', include(router.urls)),
    path('users/subscriptions/', FollowListView.as_view(), name='subscriptions'),
    path(
        'users/<int:user_id>/subscribe/',
        FollowCreateDestroyView.as_view(),
        name='subscribe'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteCreateDestroyView.as_view(),
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartCreateDestroyView.as_view(),
    ),
]