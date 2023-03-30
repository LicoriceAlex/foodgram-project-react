from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import RecipeFilter, IngredientFilter
from api.pagination import PageNumberPaginationWithLimit
from api.permissions import IsAuthorOrAuthenticatedOrReadOnly
from foodgram.models import (Cart, Favorites, Ingredient, IngredientAmount,
                             Recipe, Tag)
from foodgram.serializers.additional_serializers import RecipeShortSerializer
from foodgram.serializers.serializers import (IngredientSerializer,
                                              RecipeGetSerializer,
                                              RecipePostPatchDelSerializer,
                                              TagSerializer,
                                              CartSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['^name']


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для тегов"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов"""
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPaginationWithLimit
    permission_classes = (IsAuthorOrAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipePostPatchDelSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        data = {
            "user": user.pk,
            "recipe": pk
        }
        serializer = CartSerializer(data=data)
        if (request.method == 'POST'
                and serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        recipe_in_cart = get_object_or_404(Cart, user=user, recipe=recipe)
        recipe_in_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        list_of_products = 'Список продуктов:'
        ingredients = IngredientAmount.objects.filter(
            recipe__in_carts__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        for ingredient in ingredients:
            list_of_products += (
                f'\n{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}'
            )
        file = 'list_of_products.txt'
        response = HttpResponse(list_of_products, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            Favorites.objects.create(recipe=recipe, user=request.user)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        Favorites.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
