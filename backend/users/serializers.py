from rest_framework import serializers
from .models import User, Follow
from foodgram.models import Recipe
from django.db.models import F
from django.contrib.auth.password_validation import validate_password


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserGetSerializer(serializers.ModelSerializer):
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


class UserSetPasswordSerializer(serializers.BaseSerializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

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
    """ Сериализатор для отображения подписок пользователя. """

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

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return FollowGetSerializer(
            recipes, many=True, context={'request': request}).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


# class SubscriptionSerializer(serializers.ModelSerializer):
#     """ Сериализатор подписок. """

#     class Meta:
#         model = Subscription
#         fields = ['user', 'author']
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Subscription.objects.all(),
#                 fields=['user', 'author'],
#             )
#         ]

#     def to_representation(self, instance):
#         return ShowSubscriptionsSerializer(instance.author, context={
#             'request': self.context.get('request')
#         }).data
