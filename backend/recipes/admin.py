from django import forms
from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeForm(forms.ModelForm):
    favorited_times = forms.IntegerField(
        widget=forms.NumberInput(attrs={'readonly': 'readonly'}),
        initial=0,
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'name',
            'text',
            'image',
            'cooking_time',
            'tags',
            'favorited_times',
        )

    def get_initial_for_field(self, field, field_name):
        initial = super().get_initial_for_field(field, field_name)
        if (
                field_name == 'favorited_times'
                and self.instance in Recipe.objects.all()
        ):
            initial = self.instance.subscribers.count()
        return initial


class RecipeIngredientInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError('Добавьте хотя бы один ингредиент')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    formset = RecipeIngredientInlineFormset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',)
    list_filter = ('author', 'name', 'tags',)
    list_display_links = ('id', 'name',)
    form = RecipeForm
    inlines = (RecipeIngredientInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(RecipeIngredient)
