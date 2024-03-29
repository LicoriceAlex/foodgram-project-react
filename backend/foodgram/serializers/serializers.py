from django.shortcuts import get_object_or_404
from rest_framework import serializers

from foodgram.models import (Cart, Favorites, Ingredient, IngredientAmount,
                             Recipe, Tag)
from users.serializers import UserGetSerializer

from .additional_serializers import Base64ImageField


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор колличества ингредиента в рецепте"""
    id = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тега"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для представления рецепта"""
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientInRecipeReadSerializer(
        source='ingredient_amount',
        many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        return user.is_authenticated and Favorites.objects.filter(
            user=user, recipe=recipe.id
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return user.is_authenticated and Cart.objects.filter(
            user=user, recipe=recipe.id
        ).exists()


class RecipePostPatchDelSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate(self, data):
        tags_len = len(data['tags'])
        if tags_len == 0:
            raise serializers.ValidationError(
                'Нельзя создать рецепт без тегов'
            )
        if tags_len != len(set(data['tags'])):
            raise serializers.ValidationError(
                'Теги должны быть уникальными'
            )
        ingredients_id = []
        for ingredient in data['ingredients']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Колличество ингридиента не может быть меньше одного'
                )
            ingredients_id.append(ingredient['id'])
        if len(ingredients_id) > len(set(ingredients_id)):
            raise serializers.ValidationError(
                'Ингридиенты должны быть уникальными'
            )
        if data['cooking_time'] == 0:
            raise serializers.ValidationError(
                'Время приготовления не может быть равно нулю'
            )
        return data

    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_amounts(recipe=recipe,
                                        ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients_amounts(recipe=instance,
                                        ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(instance,
                                   context=context).data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины"""

    class Meta:
        model = Cart
        fields = ('user', 'recipe',)

    def create(self, validated_data):
        if Cart.objects.filter(
                user=validated_data['user'],
                recipe=validated_data['recipe']).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в список покупок'
            )
        return Cart.objects.create(**validated_data)
