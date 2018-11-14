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


class Permission(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('member', 'project')]