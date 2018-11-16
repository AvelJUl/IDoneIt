from django.utils.html import format_html

from idoneit import admin
from django.contrib import admin as _admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.models import Role


class RoleAdmin(_admin.ModelAdmin):
    """
    Class for admin generic views of Role model.
    """
    fieldsets = (
        (None, {'fields': ('name',)}),
        (_('Project permissions'), {'fields': ('edit_project',)}),
        (_('Issue permissions'), {'fields': ('create_issue', 'edit_issue', 'delete_issue')}),
        (_('Issue permissions'), {'fields': ('create_meeting', 'edit_meeting', 'delete_meeting')}),
    )
    list_display = ('name', 'edit_project', 'create_issue', 'edit_issue', 'delete_issue',
                    'create_meeting', 'edit_meeting', 'delete_meeting', 'account_actions')
    search_fields = ('name',)
    ordering = ('-id',)
    list_filter = ('edit_project', 'create_issue', 'edit_issue', 'delete_issue', 'create_meeting',
                   'edit_meeting', 'delete_meeting')

    def get_queryset(self, request):
        qs = super(RoleAdmin, self).get_queryset(request)
        return qs.filter(created_by_id=request.user.id)

    def account_actions(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-default">View</a>&nbsp;\
            <a href="{}" class="btn btn-info">Edit</a>&nbsp;\
            <a href="{}" class="btn btn-danger">Delete</a>',
            reverse('admin:core_role_change', args=[obj.pk]),
            reverse('admin:core_role_change', args=[obj.pk]),
            reverse('admin:core_role_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"

    def save_model(self, request, obj, form, change):
        obj.created_by_id = request.user.id
        super().save_model(request, obj, form, change)


# Re-register UserAdmin
admin.admin_site.register(Role, RoleAdmin)