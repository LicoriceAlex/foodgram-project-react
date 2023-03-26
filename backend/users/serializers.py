from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Follow, User
from foodgram.models import Recipe
from foodgram.serializers.additional_serializers import RecipeShortSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserCreateSerializer, self).create(validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return UserGetSerializer(instance,
                                 context=context).data


class UserGetSerializer(serializers.ModelSerializer):
    """Сериализатор отображения пользователя"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, user):
        request = self.context.get('request')
        return (request is not None
                and request.user.is_authenticated and Follow.objects.filter
                (user=request.user, author=user).exists())


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
        return (request is not None
                and request.user.is_authenticated and Follow.objects.filter
                (user=request.user, author=author).exists())

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


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписки"""

    class Meta:
        model = Follow
        fields = ('user', 'author',)

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data

    def create(self, validated_data):
        if Follow.objects.filter(
                user=validated_data['user'],
                author=validated_data['author']).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя'
            )
        return Follow.objects.create(**validated_data)
