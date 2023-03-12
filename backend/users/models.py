from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# USER = "user"
# ADMIN = "admin"
# ROLES = [
#     ("user", USER),
#     ("admin", ADMIN)
# ]


class CustomUser(AbstractUser):
    """Класс пользователей."""
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты',
        unique=True)
    username = models.CharField(
        max_length=150,
        verbose_name='Уникальный юзернейм',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль'
    )
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
