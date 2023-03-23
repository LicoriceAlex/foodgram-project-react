from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=10
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(
        verbose_name='Название тега',
        max_length=20,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=16,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Адрес тега',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег',
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}, цвет - {self.color}'


class Recipe(models.Model):
    """Модель рецепта"""
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    text = models.CharField(
        verbose_name='Описание',
        max_length=1000
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        verbose_name='Время публикации',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reciepes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты блюда',
        related_name='recipes',
        through='foodgram.IngredientAmount',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фотография',
        null=True,
        default=None
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт',
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class IngredientAmount(models.Model):
    """Промежуточная модель для связи рецепта с ингредиентом.
    Указывается кол-во ингедиента в рецепте"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        related_name='ingredient_amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_amount'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Колличество ингридиента'
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Колличество ингридиента в рецепте',
        verbose_name_plural = 'Колличество ингридиентов в рецепте'

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.amount}'


class Favorites(models.Model):
    """Модель добавления рецепта в избранное"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Избранные рецепты',
        related_name='in_favorites',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites',
    )
    date = models.DateTimeField(
        verbose_name='Время добавления в избранное',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='рецепт уже есть в избранном')
        ]

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'


class Cart(models.Model):
    """Модель добавления рецепта в корзину"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты в корзине',
        related_name='in_carts',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец корзины',
        related_name='cart',
    )
    date = models.DateTimeField(
        verbose_name='Время добавления в корзину',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзинах'
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'],
                                    name='рецепт уже есть в корзине')
        ]

    def __str__(self) -> str:
        return f'{self.user} -> {self.recipe}'
