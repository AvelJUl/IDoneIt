from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User


class UserRegistrationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus first name, last name and email."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')