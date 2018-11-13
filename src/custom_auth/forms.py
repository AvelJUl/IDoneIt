from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    User registration form class. Extends default UserCreationForm class.
    Email was added to required fields.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')