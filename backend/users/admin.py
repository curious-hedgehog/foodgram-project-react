from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserModelAdmin(UserAdmin):
    list_filter = ('is_staff', 'is_superuser', 'is_active',
                   'groups', 'email', 'username',)
    filter_horizontal = ('groups', 'user_permissions', 'favorites',
                         'shopping_cart', 'followings',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Рецепты'), {'fields': ('favorites', 'shopping_cart')}),
        (_('Подписки'), {'fields': ('followings',)}),
    )
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    list_display_links = ('id', 'username',)


admin.site.register(User, UserModelAdmin)
