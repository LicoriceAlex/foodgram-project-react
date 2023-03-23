from django.contrib import admin

from .models import Cart, Favorites, Ingredient, IngredientAmount, Recipe, Tag

# ругается isort, если делать построчный импорт


class IngredientAmountInLine(admin.StackedInline):
    model = IngredientAmount
    extra = 1


class FavoritesInLine(admin.StackedInline):
    model = Favorites


class CartInLine(admin.StackedInline):
    model = Cart


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInLine, FavoritesInLine, CartInLine)
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'pub_date',
        'get_favorites',
    )

    def get_favorites(self, recipe):
        return recipe.in_favorites.count()

    get_favorites.short_description = 'Добавлений в избранное'
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'name', 'tags')
    search_fields = ('author', 'name', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorites)
admin.site.register(Cart)
