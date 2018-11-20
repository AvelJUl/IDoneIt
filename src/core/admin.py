from django.utils.html import format_html

from custom_auth.models import User
from idoneit import admin
from django.contrib import admin as _admin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.models import Role, Project, Permission, Issue, Meeting


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
            reverse('admin_site:core_role_change', args=[obj.pk]),
            reverse('admin_site:core_role_change', args=[obj.pk]),
            reverse('admin_site:core_role_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"

    def save_model(self, request, obj, form, change):
        obj.created_by_id = request.user.id
        super().save_model(request, obj, form, change)


admin.admin_site.register(Role, RoleAdmin)


class PermissionInline(_admin.TabularInline):
    model = Permission
    fields = ['member', 'role']


class ProjectAdmin(_admin.ModelAdmin):
    """
    Class for admin generic views of Role model.
    """
    fieldsets = ((_('Project information'), {'fields': ('name', 'description')}),)
    inlines = [PermissionInline,]
    list_display = ('name', 'description', 'account_actions')
    search_fields = ('name',)
    ordering = ('-id',)


    def account_actions(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-default">View</a>&nbsp;\
            <a href="{}" class="btn btn-info">Edit</a>&nbsp;\
            <a href="{}" class="btn btn-danger">Delete</a>',
            reverse('admin_site:core_project_change', args=[obj.pk]),
            reverse('admin_site:core_project_change', args=[obj.pk]),
            reverse('admin_site:core_project_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"

    def save_model(self, request, obj, form, change):
        obj.created_by_id = request.user.id
        super().save_model(request, obj, form, change)


admin.admin_site.register(Project, ProjectAdmin)


class IssueAdmin(_admin.ModelAdmin):
    """
    Class for admin generic views of Role model.
    """
    fieldsets = ((_('Issue information'), {'fields': ('tracker', 'subject', 'description')}),
                 (_('Additional information'), {'fields': ('status', 'related_to', 'progress', 'update')}),)
    list_display = ('tracker', 'subject', 'description', 'status', 'update', 'account_actions')
    search_fields = ('subject',)
    ordering = ('-id',)
    list_filter = ('tracker', 'status')

    def account_actions(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-default">View</a>&nbsp;\
            <a href="{}" class="btn btn-info">Edit</a>&nbsp;\
            <a href="{}" class="btn btn-danger">Delete</a>',
            reverse('user_site:core_issue_change', args=[obj.pk]),
            reverse('user_site:core_issue_change', args=[obj.pk]),
            reverse('user_site:core_issue_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"


admin.user_site.register(Issue, IssueAdmin)


class MeetingAdmin(_admin.ModelAdmin):
    """
    Class for admin generic views of Role model.
    """
    fieldsets = ((_('Meeting information'), {'fields': ('project', 'subject', 'place', 'date_and_time', 'members')}),)
    list_display = ('subject', 'place', 'date_and_time')
    search_fields = ('subject',)
    list_filter = ('project',)
    ordering = ('-id',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(created_by_id=request.user.created_by_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def account_actions(self, obj):
        return format_html(
            '<a href="{}" class="btn btn-default">View</a>&nbsp;\
            <a href="{}" class="btn btn-info">Edit</a>&nbsp;\
            <a href="{}" class="btn btn-danger">Delete</a>',
            reverse('user_site:core_meeting_change', args=[obj.pk]),
            reverse('user_site:core_meeting_change', args=[obj.pk]),
            reverse('user_site:core_meeting_delete', args=[obj.pk]),
        )

    account_actions.allow_tags = True
    account_actions.short_description = "Account actions"


admin.user_site.register(Meeting, MeetingAdmin)