from rest_framework import serializers
from foodgram.models import (Ingredient, Tag, Recipe,
                             Favorites, Cart, IngredientAmount)
from .services import Base64ImageField
from django.db.models import F
from users.serializers import UserGetSerializer


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
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

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_amount__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=user, recipe=recipe.id
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(
            user=user, recipe=recipe.id
        ).exists()


class RecipePostPatchDelSerializer(serializers.ModelSerializer):
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

    # def validate_ingredients(self, value):
    #     ingredients = value
    #     if not ingredients:
    #         raise ValidationError({
    #             'ingredients': 'Нужен хотя бы один ингредиент!'
    #         })
    #     ingredients_list = []
    #     for item in ingredients:
    #         ingredient = get_object_or_404(Ingredient, id=item['id'])
    #         if ingredient in ingredients_list:
    #             raise ValidationError({
    #                 'ingredients': 'Ингридиенты не могут повторяться!'
    #             })
    #         if int(item['amount']) <= 0:
    #             raise ValidationError({
    #                 'amount': 'Количество ингредиента должно быть больше 0!'
    #             })
    #         ingredients_list.append(ingredient)
    #     return value

    # def validate_tags(self, value):
    #     tags = value
    #     if not tags:
    #         raise ValidationError({
    #             'tags': 'Нужно выбрать хотя бы один тег!'
    #         })
    #     tags_list = []
    #     for tag in tags:
    #         if tag in tags_list:
    #             raise ValidationError({
    #                 'tags': 'Теги должны быть уникальными!'
    #             })
    #         tags_list.append(tag)
    #     return value
###
    def create_ingredients_amounts(self, ingredients, recipe):
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
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


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time',)
