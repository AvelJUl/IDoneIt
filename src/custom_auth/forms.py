from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Форма создания учётной записи пользователя. Включает все необходимые
    поля и имя, фамилию и email пользователя.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')