from django.forms import MultipleChoiceField
from django.forms.fields import CharField
from django_filters import Filter
from django_filters import rest_framework as filters
from django_filters.constants import EMPTY_VALUES

from recipes.models import Recipe


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

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        lookup = "%s__%s" % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(**{lookup: value}).distinct()
        return qs


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(field_name='author')
    tags = MultipleValueFilter(field_name='tags__slug', field_class=CharField)
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )
    is_favorited = filters.NumberFilter(
        method='filter_is_favorited'
    )

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.auth or value != 1:
            return queryset
        return queryset & self.request.user.shopping_cart.all()

    def filter_is_favorited(self, queryset, name, value):
        if not self.request.auth or value != 1:
            return queryset
        return queryset & self.request.user.favorites.all()

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
