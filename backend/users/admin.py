from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
