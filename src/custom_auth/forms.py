from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    User registration form class. Extends default UserCreationForm class.
    Email was added to required fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')