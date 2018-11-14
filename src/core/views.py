from django.contrib.admin.helpers import Fieldset
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import HttpResponseRedirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View

from custom_auth.models import User
from custom_auth.forms import UserRegistrationForm


class UserCreate(CreateView):
    """
    Generic view class for creating new user through registration form.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'idoneit/core/user/create_form.html'
    success_url = reverse_lazy('admin_user_list')
    extra_context = {
        'title': _("New user registration")
    }

    @method_decorator(login_required(login_url='login/'))
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

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.is_staff = False
        self.object.created_by_id = self.request.user.id
        self.object.save()


class UserList(ListView):
    """
    Generic list view to show all shared templates in grid view.
    """
    model = User
    template_name = 'idoneit/core/user/list_form.html'
    ordering = 'id'

    @method_decorator(login_required(login_url='login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = super().get_queryset()
        user = self.kwargs.get('user')
        search_query = self.request.GET.get('q')
        if user is not None:
            self.queryset = self.queryset.filter(created_by_id=user.id)
        return self.queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        extra_content = {}
        search_query = self.request.GET.get('q')
        if search_query is not None:
            extra_content.update({'search_query': search_query})
        context.update(extra_content)
        return context
