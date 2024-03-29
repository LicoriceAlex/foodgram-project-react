from django.contrib.auth import get_user_model
from django_filters.rest_framework import (CharFilter, FilterSet,
                                           ModelChoiceFilter,
                                           ModelMultipleChoiceFilter,
                                           NumberFilter)

from foodgram.models import Ingredient, Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    """Фильтр рецепта"""
    is_favorited = NumberFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = NumberFilter(
        method='get_is_in_shopping_cart'
    )
    author = ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags',)

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_carts__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    name = CharFilter(method='search_ingredient')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def search_ingredient(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(name__icontains=value).order_by('name')
