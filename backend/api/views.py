from collections import defaultdict

from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.models import Ingredient, Recipe, Tag
from api.permissions import IsOwnerOrAdminOrReadOnly
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeShortSerializer, RecipeWriteSerializer,
                             TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    filterset_class = RecipeFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        result_serializer = RecipeSerializer(
            recipe, context={'request': request}
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            result_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        result_serializer = RecipeSerializer(
            recipe, context={'request': request}
        )

        return Response(result_serializer.data)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return RecipeSerializer
        return RecipeWriteSerializer


class FavoriteView(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = RecipeShortSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs['recipe_id'])
        if (
                not recipe.exists()
                or recipe.first() in request.user.favorites.all()
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe.first()
        request.user.favorites.add(recipe)
        serializer = self.get_serializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        if recipe not in request.user.favorites.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = RecipeShortSerializer
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs['recipe_id'])
        if (
                not recipe.exists()
                or recipe.first() in request.user.shopping_cart.all()
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe.first()
        request.user.shopping_cart.add(recipe)
        serializer = self.get_serializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        if recipe not in request.user.favorites.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.shopping_cart.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):

    if not request.auth:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    pieces = request.user.shopping_cart.values_list(
        'ingredients__ingredient', 'ingredients__amount'
    )
    total_amounts = defaultdict(int)
    for ingredient, amount in pieces:
        total_amounts[ingredient] += amount
    ingredients = Ingredient.objects.filter(id__in=total_amounts)
    pieces_response_list = []
    for ingredient in ingredients:
        pieces_response_list.append(
            f'{ingredient.name}: {total_amounts[ingredient.id]} '
            f'{ingredient.measurement_unit}\n'
        )
    response_text = ''.join(pieces_response_list)
    return Response(response_text, status=status.HTTP_200_OK)
