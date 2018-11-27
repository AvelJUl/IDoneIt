from django.contrib.admin import AdminSite as _AdminSite, register as _register
from django.utils.translation import gettext_lazy as _
from custom_auth.auth import UserAdminAuthenticationForm


class AdminSite(_AdminSite):
    """
    Переопределение сайта администратора.
    """
    # Текст в заголовке каждой страницы.
    site_title = _('IDoneIt site admin')

    # Текст на панели усправления
    site_header = _('IDoneIt administration')

    # Шаблон входа в кабинет администратора
    login_template = 'admin/registration/login.html'


admin_site = AdminSite(name='admin_site')


class UserSite(_AdminSite):
    """
    Переопределение сайта администратора для использования в качестве кабинета пользователя.
    """
    # Текст в заголовке каждой страницы.
    site_title = _('IDoneIt')

    # Текст на панели усправления
    site_header = _('IDoneIt workspace')

    # Текст, отображаемый на главной странице.
    index_title = _('Workspace')

    # Форма авторизации.
    login_form = UserAdminAuthenticationForm

    # Шаблон входа в кабинет администратора
    login_template = 'admin/registration/login.html'

    # Ограничение на вход в кабинет польщователя.
    def has_permission(self, request):
        """
        Исключение проверки is_staff
        """
        return not request.user.is_staff and not request.user.is_anonymous


user_site = UserSite(name='user_site')
