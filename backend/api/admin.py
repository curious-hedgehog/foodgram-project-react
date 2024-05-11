from django.contrib import admin
from django import forms

from api.models import Tag, Ingredient, Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    favorited_times = forms.IntegerField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Recipe
        fields = ('author', 'name', 'text', 'image',
                  'cooking_time', 'tags', 'favorited_times',)

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)
        if field_name == 'favorited_times':
            initial = self.instance.favorited_times
        return initial


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',)
    list_filter = ('author', 'name', 'tags',)
    list_display_links = ('id', 'name',)
    form = RecipeForm


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    # list_filter = ('name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
