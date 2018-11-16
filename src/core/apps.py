from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    """
    Configuration class of 'core' application.
    """
    name = 'core'
    verbose_name = _("Core of application")
