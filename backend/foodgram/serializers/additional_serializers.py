from api.services import Base64ImageField
from foodgram.models import Recipe
from rest_framework import serializers


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для уменьшенного представления рецепта"""
    image = Base64ImageField

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time',)
