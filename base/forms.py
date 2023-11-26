from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, PointTransaction
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class AwardForm(ModelForm):

    class Meta:
        model = PointTransaction
        fields = '__all__'


class CustomAuthenticationForm(AuthenticationForm):
    # Add any additional fields or customization you need
    pass