from django.contrib import admin

from .models import Ingredient, Tag, IngredientAmount, Recipe, Favorites, Cart


class IngredientAmountInLine(admin.StackedInline):
    model = IngredientAmount
    extra = 1


class FavoritesInLine(admin.StackedInline):
    model = Favorites


class CartInLine(admin.StackedInline):
    model = Cart


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInLine, FavoritesInLine, CartInLine)


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites)
admin.site.register(Cart)
