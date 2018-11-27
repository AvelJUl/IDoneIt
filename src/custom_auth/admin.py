from django.utils.html import format_html

from idoneit import admin
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User


class UserAdmin(_UserAdmin):
    """
    Класс, который генерирует отобржение CRUD шаблонов модели
    Пользователя в кабинете администратора.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'account_actions')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-id',)
    list_filter = ()

    # Получение множества пользователе для отображение списка пользователей.
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        return qs.filter(created_by_id=request.user.id, is_staff=False)

    def account_actions(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-default">View</a>&nbsp;\
            <a href="{}" class="btn btn-info">Edit</a>&nbsp;\
            <a href="{}" class="btn btn-danger">Delete</a>',
            reverse('admin_site:custom_auth_user_change', args=[obj.pk]),
            reverse('admin_site:custom_auth_user_change', args=[obj.pk]),
            reverse('admin_site:custom_auth_user_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"

    # При создании пользователя из кабинета администратора поле is_staff=False.
    def save_model(self, request, obj, form, change):
        obj.created_by_id = request.user.id
        obj.is_staff = False
        super().save_model(request, obj, form, change)


# Регистрация модели Пользователя в кабинете администратора.
admin.admin_site.register(User, UserAdmin)