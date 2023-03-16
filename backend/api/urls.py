from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView

from foodgram.views import IngredientViewSet, TagViewSet, RecipeViewSet
# from .views import IngredientViewSet, TagViewSet, RecipeViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    # path('', include('djoser.urls')),

    path('auth/token/login/', TokenCreateView.as_view()),
    path('auth/token/logout/', TokenDestroyView.as_view()),
]
