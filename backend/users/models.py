from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


USER = "user"
ADMIN = "admin"
ROLES = [
    ("user", USER),
    ("admin", ADMIN)
]


# class MyUserManager(UserManager):
#     """Сохраняет пользователя только с email.
#     Зарезервированное имя использовать нельзя."""
#     def create_user(self, username, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Поле email обязательное')
#         if username == reserved_name:
#             raise ValueError(message_for_reservad_name)
#         return super().create_user(
#             username, email=email, password=password, **extra_fields)

#     def create_superuser(
#             self, username, email, password, role='admin', **extra_fields):
#         return super().create_superuser(
#             username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
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
    REQUIRED_FIELDS = ('__all__',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER
