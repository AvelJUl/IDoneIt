from django.db import models
from django.contrib.auth.models import Permission as _Permission
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User
from core.consts import TRACKERS, STATUSES


class Project(models.Model):
    """
    Класс, используемый для описания сущности "Проект".
    """
    # Наименование проекта.
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A project with that name already exists."),
        },
    )
    # Описание проекта.
    description = models.TextField(_('description'), null=True, blank=True)
    # Пользователь, которым был создан проект.
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    # При выводе объекта выводить только наименование.
    def __str__(self):
        return self.name


class Role(models.Model):
    """
    Класс, используемый для описания сущности "Роль".
    """
    # Наименование роли.
    name = models.CharField(
        _('name'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A role with that name already exists."),
        },
    )
    # Возможность редактирования информации о проекте.
    edit_project = models.BooleanField(_('edit project'), default=False)
    # Возможность создания задачи.
    create_issue = models.BooleanField(_('create issue'), default=False)
    # Возможность редактирования информации о задаче.
    edit_issue = models.BooleanField(_('edit issue'), default=False)
    # Возможность удаления информации о задаче.
    delete_issue = models.BooleanField(_('delete issue'), default=False)
    # Возможность создания встречи.
    create_meeting = models.BooleanField(_('create meeting'), default=False)
    # Возможность редактирования информации о встрече.
    edit_meeting = models.BooleanField(_('edit meeting'), default=False)
    # Возможность удаления информации о встрече.
    delete_meeting = models.BooleanField(_('delete meeting'), default=False)

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    # При выводе объекта выводить только наименование.
    def __str__(self):
        return 'Role "' + self.name + '"'


class Permission(models.Model):
    """
    Класс, используемый для описания отношений между проектов, его участником
    с назначенной ему ролью.
    """
    # Участник.
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    # Проект.
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # Роль.
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = [('member', 'project'), ('member', 'role')]

    def __str__(self):
        return self.role.name + ': ' + self.member.username


class DecimalFieldRange(models.DecimalField):
    """
    Переопределение класса вещественных чисел для описания
    процента выполнения задачи.

    Добавлены максимальное и минимальное значение.
    """
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, *args, **kwargs):
        super(DecimalFieldRange, self).__init__(*args, **kwargs)
        self.min_value, self.max_value = min_value, max_value

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(DecimalFieldRange, self).formfield(**defaults)


class Issue(models.Model):
    """
    Класс, используемый для описания сущности "Задача".
    """
    # Предмает задачи.
    subject = models.CharField(
        _('subject'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A issue with that subject already exists."),
        },
    )
    # Описание задачи.
    description = models.TextField( _('description'), null=True, blank=True)
    # Трекер задачи.
    tracker = models.CharField(_('tracker'), max_length=14,  choices=TRACKERS)
    # Статус задачи.
    status = models.CharField(_('status'), max_length=14, choices=STATUSES)
    # Пользователь, которому назначена задача.
    related_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # Прогресс задачи.
    progress = DecimalFieldRange(_('progress'), default=0.0, max_digits=3, decimal_places=2,
                                 max_value=1.0, min_value=0.0)
    # Дата обновления задачи.
    update = models.DateTimeField(_('update'), default=0)
    # Проект с которым связана задача.
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = _('issue')
        verbose_name_plural = _('issues')

    # При выводе объекта выводить только наименование.
    def __str__(self):
        return 'Issue "' + self.subject + '"'


class Meeting(models.Model):
    """
    Класс, используемый для описания сущности "Встречи".
    """
    # Предмает встречи.
    subject = models.CharField(
        _('subject'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A meeting with that subject already exists."),
        },
    )
    # Место встречи.
    place = models.TextField(_('place'), null=True, blank=True)
    # Время и дата встречи.
    date_and_time = models.DateTimeField(_('date and time'), default=0)
    # Участники встречи.
    members = models.ManyToManyField(User)
    # Проект, с которым связана встречи.
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = _('meeting')
        verbose_name_plural = _('meetings')

    # При выводе объекта выводить только наименование.
    def __str__(self):
        return 'Meeting: ' + self.subject
