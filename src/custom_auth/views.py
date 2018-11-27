from django.contrib.admin.helpers import Fieldset
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView

from custom_auth.models import User
from custom_auth.forms import UserRegistrationForm


class RegistrationView(CreateView):
    """
    Класс, который генерирует отображение страницы регистрации ного пользователя.
    """
    # Модель пользователя.
    model = User
    # Форма регистрации пользователя.
    form_class = UserRegistrationForm
    # Шаблон страницы регистрации пользователя.
    template_name = 'registration/registration_form.html'
    # Url, куда будет перенаправлен пользователь в случае успешной регистрации.
    success_url = reverse_lazy('admin_site:login')
    # Заголовок шаблона.
    extra_context = {
        'title': _("New administrator registration")
    }

    """
    Запрос на отображение страницы регистрации пользователя.
    В случае, если пользователь авторизирован, перенаправлять его на главную страницу.
    """
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url=reverse_lazy('admin:index')))
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fieldset'] = Fieldset(
            form=context['form'],
            name=None,
            readonly_fields=(),
            classes=('wide',),
            fields=self.form_class.Meta.fields
        )
        return context

    """
    POST-запрос. При сохранении данных о новом пользователе установление is_staff в значение True.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if self.object is not None:
            self.object.is_staff = True
            self.object.created_by_id = self.object.id
            self.object.save()
        return response
