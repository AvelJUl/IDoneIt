from django.contrib.admin import AdminSite as _AdminSite, register as _register
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class AdminSite(_AdminSite):
    """
    Overriding of default AdminSite with custom title, header and url values.
    """
    # Text to put at the end of each page's <title>.
    site_title = _('IDoneIt site admin')

    # Text to put in each page's <h1>.
    site_header = _('IDoneIt administration')


admin_site = AdminSite(name='admin_site')
