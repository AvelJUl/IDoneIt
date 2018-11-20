from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User
from core.consts import TRACKERS, STATUSES


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


class DecimalFieldRange(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, *args, **kwargs):
        super(DecimalFieldRange, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(DecimalFieldRange, self).formfield(**defaults)


class Issue(models.Model):
    subject = models.CharField(
        _('subject'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A subject with that name already exists."),
        },
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )
    tracker = models.CharField(_('tracker'), max_length=14,  choices=TRACKERS)
    status = models.CharField(_('status'), max_length=14, choices=STATUSES)
    related_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    progress = DecimalFieldRange(_('progress'), default=0.0, max_digits=3, decimal_places=2, max_value=1.0, min_value=0.0)
    update = models.DateTimeField(_('update'), default=0)
    #project_id = models.IntegerField(_('created_by_id'), default=0)

    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')


class Meeting(models.Model):
    subject = models.CharField(
        _('subject'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A subject with that name already exists."),
        },
    )
    place = models.TextField(
        _('place'),
        null=True,
        blank=True
    )
    date_and_time = models.DateTimeField(_('date and time'), default=0)
    members = models.ManyToManyField(User)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')