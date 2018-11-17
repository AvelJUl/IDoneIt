from django.db import models
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User


class Project(models.Model):
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A project with that name already exists."),
        },
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )
    created_by_id = models.IntegerField(_('created_by_id'), default=0)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')


class Role(models.Model):
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A role with that name already exists."),
        },
    )
    edit_project = models.BooleanField(_('edit project'), default=False)
    create_issue = models.BooleanField(_('create issue'), default=0)
    edit_issue = models.BooleanField(_('edit issue'), default=0)
    delete_issue = models.BooleanField(_('delete issue'), default=0)
    create_meeting = models.BooleanField(_('create meeting'), default=0)
    edit_meeting = models.BooleanField(_('edit meeting'), default=0)
    delete_meeting = models.BooleanField(_('delete meeting'), default=0)
    created_by_id = models.IntegerField(_('created_by_id'), default=0)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class Permission(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('member', 'project')]