from api.serializers import (IngredientSerializer, RecipeGetSerializer,
                             RecipePostPatchDelSerializer, TagSerializer,
                             RecipeShortSerializer)
from foodgram.models import Cart, Favorites, Ingredient, Recipe, Tag
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)


class IngredientViewSet(ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(ReadOnlyModelViewSet):
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
        recipe = Recipe.objects.get_object_or_404(pk=pk)
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
        recipe = get_object_or_404(Recipe, pk=pk)
        existing_in_favorites = Favorites.objects.filter(
            recipe=recipe,
            user=request.user
        ).exists()
        if request.method == 'POST':
            if existing_in_favorites:
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorites.objects.create(recipe=recipe, user=request.user)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            if not existing_in_favorites:
                return Response(
                    {'errors': 'Рецепт не добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorites.objects.filter(recipe=recipe, user=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
