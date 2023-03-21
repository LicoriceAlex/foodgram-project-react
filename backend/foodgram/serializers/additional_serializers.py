from foodgram.models import Recipe
from rest_framework import serializers
from api.services import Base64ImageField


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для уменьшенного представления рецепта"""
    image = Base64ImageField

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time',)
