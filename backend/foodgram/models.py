from djangoHexadecimal.fields import HexadecimalField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=10
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


# class Recipe(models.Model):
#     page = models.IntegerField()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=20
    )
    color = HexadecimalField(
        verbose_name='Цвет тега',
        max_length=10
    )
    slug = models.SlugField(
        verbose_name='Адрес тега',
        max_length=30
    )
