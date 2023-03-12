from .serializers import UserCreateSerializer, UserGetSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS
from .models import User


class UserViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return UserGetSerializer
        return UserCreateSerializer
