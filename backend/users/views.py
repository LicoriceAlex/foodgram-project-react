from api.pagination import PageNumberPaginationWithLimit
from api.permissions import IsAuthenticatedOrListOnly
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Follow
from .serializers import (FollowGetSerializer, UserCreateSerializer,
                          UserGetSerializer, UserSetPasswordSerializer)

User = get_user_model()


class UserViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    """Вьюсет пользователя"""
    queryset = User.objects.all()
    pagination_class = PageNumberPaginationWithLimit
    permission_classes = (IsAuthenticatedOrListOnly,)

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
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Follow.objects.create(user=user, author=author)
            serializer = FollowGetSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписаться от себя'},
                status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if not follow.exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
