from django.contrib.admin import AdminSite as _AdminSite, register as _register
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from custom_auth.auth import UserAdminAuthenticationForm


class AdminSite(_AdminSite):
    """
    Overriding of default AdminSite with custom title and header values.
    """
    # Text to put at the end of each page's <title>.
    site_title = _('IDoneIt site admin')

    # Text to put in each page's <h1>.
    site_header = _('IDoneIt administration')


admin_site = AdminSite(name='admin_site')


class UserSite(_AdminSite):
    """
    Overriding of default AdminSite with custom title and header values.
    """
    # Text to put at the end of each page's <title>.
    site_title = _('IDoneIt')

    # Text to put in each page's <h1>.
    site_header = _('IDoneIt workspace')

    # Text to put in index page's <h1>.
    index_title = _('Workspace')

    # Subclass of AuthenticationForm that will be used by the admin site login view.
    login_form = UserAdminAuthenticationForm

    # Returns True if the user for the given HttpRequest has permission to view at least one page in the admin site.
    def has_permission(self, request):
        """
        Removed check for is_staff and is_superuser.
        """
        return not request.user.is_staff and not request.user.is_anonymous


user_site = UserSite(name='user_site')
