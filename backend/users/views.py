from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from .models import Follow
from .serializers import (
    FollowGetSerializer,
    UserCreateSerializer,
    UserGetSerializer,
    UserSetPasswordSerializer,
    FollowSerializer
)
from api.mixins import CustomUserViewSet
from api.pagination import PageNumberPaginationWithLimit
from api.permissions import IsAuthenticatedOrListOnly


User = get_user_model()


class UserViewSet(CustomUserViewSet):
    """Вьюсет пользователя"""
    queryset = User.objects.all()
    pagination_class = PageNumberPaginationWithLimit
    # permission_classes = (IsAuthenticatedOrListOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserGetSerializer
        return UserCreateSerializer

    @action(detail=False,
            permission_classes=(IsAuthenticated,),
            methods=['post'])
    def set_password(self, request):
        user = request.user
        serializer = UserSetPasswordSerializer(
            data=request.data,
            context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get'])
    def me(self, request):
        return Response(
            self.get_serializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False,
            permission_classes=[IsAuthenticated],
            methods=['get'])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowGetSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            permission_classes=[IsAuthenticated],
            methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        data = {
            "user": user.pk,
            "author": pk
        }
        serializer = FollowSerializer(data=data)
        if (request.method == 'POST'
                and serializer.is_valid(raise_exception=True)):
            serializer.save()
            serializer = FollowGetSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data)

        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
