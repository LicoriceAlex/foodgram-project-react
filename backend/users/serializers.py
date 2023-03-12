from rest_framework import serializers
from .models import User
from django.db.models import F


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return UserGetSerializer(instance, context=context).data


class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
