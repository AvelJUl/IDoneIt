from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    """
    Конфигурационный класс приложения 'core'.
    """
    name = 'core'
    verbose_name = _("Core of application")
