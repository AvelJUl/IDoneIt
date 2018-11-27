from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from custom_auth.models import User


class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Форма входа в кабинет пользователя.
    """
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = "Please enter the correct username and password for a participant account."

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache.is_staff or self.user_cache.is_anonymous:
                raise forms.ValidationError(message)
        return self.cleaned_data

