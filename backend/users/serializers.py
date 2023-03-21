from django.contrib.auth.password_validation import validate_password
from foodgram.models import Recipe
from foodgram.serializers.additional_serializers import RecipeShortSerializer
from rest_framework import serializers

from .models import Follow, User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор отображения пользователя"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, user):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        is_subscribed = Follow.objects.filter(
            user=request.user, author=user
        ).exists()
        return is_subscribed


class UserSetPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор смены пароля"""
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('new_password', 'current_password',)

    def validate_current_password(self, value):
        request = self.context.get('request')
        if request.user.check_password(value):
            return value
        else:
            raise serializers.ValidationError(
                'Неправильный пароль'
            )

    def validate_new_password(self, value):
        validate_password(value)
        return value


class FollowGetSerializer(serializers.ModelSerializer):
    """Сериализатор отображения подписок пользователя"""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=author
        ).exists()

    def get_recipes(self, author):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(author=author)
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeShortSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, author):
        return Recipe.objects.filter(author=author).count()
