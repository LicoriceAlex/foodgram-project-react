from requests import Response
from .serializers import UserCreateSerializer, UserGetSerializer, UserSetPasswordSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    # def get_serializer_class(self):
    #     if self.request.method in SAFE_METHODS:
    #         return UserGetSerializer
    #     return UserCreateSerializer

    # @action(methods=['post'], detail=True)
    # def set_password(self, request):
    #     user = self.get_object()
    #     serializer = UserSetPasswordSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(username=request.user.username)
        serializer = UserGetSerializer(request.user)
        return Response(serializer.data)
