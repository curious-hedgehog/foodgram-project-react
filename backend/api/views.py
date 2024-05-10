from collections import defaultdict

from django.forms import MultipleChoiceField
from django.forms.fields import CharField
from rest_framework import viewsets, permissions, filters, generics, status
from django_filters import rest_framework as df_filters, Filter
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import Tag, Ingredient, Recipe
from api.permissions import IsOwnerOrAdminOrReadOnly
from api.serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from users.serializers import RecipeShortSerializer


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


BOOLEAN_CHOICES = (
    (0, 'false'),
    (1, 'true'),
)


class MultipleValueField(MultipleChoiceField):
    def __init__(self, *args, field_class, **kwargs):
        self.inner_field = field_class()
        super().__init__(*args, **kwargs)

    def valid_value(self, value):
        return self.inner_field.validate(value)

    def clean(self, values):
        return values and [self.inner_field.clean(value) for value in values]


class MultipleValueFilter(Filter):
    field_class = MultipleValueField

    def __init__(self, *args, field_class, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, field_class=field_class, **kwargs)


class RecipeFilter(df_filters.FilterSet):
    author = df_filters.NumberFilter(field_name='author')
    tags = MultipleValueFilter(field_name='tags__slug', field_class=CharField)
    is_in_shopping_cart = df_filters.NumberFilter(
        method='filter_is_in_shopping_cart')
    is_favorited = df_filters.NumberFilter(
        method='filter_is_favorited')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.auth:
            return queryset
        if value == 1:
            queryset &= self.request.user.shopping_cart.all()
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if not self.request.auth:
            return queryset
        if value == 1:
            queryset &= self.request.user.favorites.all()
        return queryset

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(**{
            name: value,
        })

    class Meta:
        model = Recipe
        fields = ['author', 'tags',]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    filterset_class = RecipeFilter


class FavoriteCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = RecipeShortSerializer
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs['recipe_id'])
        if not recipe.exists() or recipe.first() in request.user.favorites.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe.first()
        request.user.favorites.add(recipe)
        serializer = self.get_serializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        if recipe not in request.user.favorites.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):

    serializer_class = RecipeShortSerializer
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs['recipe_id'])
        if not recipe.exists() or recipe.first() in request.user.shopping_cart.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = recipe.first()
        request.user.shopping_cart.add(recipe)
        serializer = self.get_serializer(recipe)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
            f'{ingredient.name}: {total_amounts[ingredient.id]} {ingredient.measurement_unit}\n'
        )
    response_text = ''.join(pieces_response_list)
    return Response(response_text, status=status.HTTP_200_OK)
