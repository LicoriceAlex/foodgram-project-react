from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Follow

User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
