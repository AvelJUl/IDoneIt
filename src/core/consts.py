from django.utils.translation import ugettext_lazy as _

# Возможные трекеры задачи.
TRACKERS = (
    ('0', _('Defect')),
    ('1', _('Feature')),
    ('2', _('Patch')),
)

# Возможные статусы задачи.
STATUSES = (
    ('0', _('New')),
    ('1', _('In Progress')),
    ('2', _('Solved')),
    ('3', _('Close')),
)