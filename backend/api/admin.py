from django.contrib import admin

from api.models import Tag, Unit, Ingredient, Recipe, RecipeIngredient

admin.site.register(Tag)
admin.site.register(Unit)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)