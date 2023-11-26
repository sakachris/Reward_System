from django.contrib.auth.forms import (
        UserCreationForm,
        UserChangeForm,
        AuthenticationForm
)
from .models import CustomUser, PointTransaction
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    """ customizing user creation form """

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """ customizing user update form """

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class AwardForm(ModelForm):
    """ point award form """

    class Meta:
        model = PointTransaction
        fields = ['student', 'category', 'description']


class CustomAuthenticationForm(AuthenticationForm):
    """ authentication form """
    pass
