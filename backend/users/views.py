from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from .models import Follow
from .serializers import (FollowGetSerializer, FollowPostDelSerializer,
                          UserCreateSerializer, UserGetSerializer,
                          UserSetPasswordSerializer)

User = get_user_model()


class UserViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserGetSerializer
        return UserCreateSerializer

    @action(detail=False,
            permission_classes=[IsAuthenticated], methods=['get'])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        # print(queryset)
        # pages = self.paginate_queryset(queryset)
        serializer = FollowGetSerializer(
            # pages,
            queryset,
            many=True,
            context={'request': request}
        )
        # return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(detail=True,
            permission_classes=[IsAuthenticated], methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Вы не можете подписаться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
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
        elif request.method == 'DELETE':
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
            elif follow.exists():
                follow.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
