from api.serializers import IngredientSerializer, TagSerializer, RecipeGetSerializer, RecipePostPatchDelSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import SAFE_METHODS
from foodgram.models import Ingredient, Tag, Recipe, Favorites, Cart
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipePostPatchDelSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            Cart.objects.create(recipe=recipe, user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Cart.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = Recipe.objects.get(pk=pk)
        if request.method == 'POST':
            Favorites.objects.create(recipe=recipe, user=request.user)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Favorites.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
