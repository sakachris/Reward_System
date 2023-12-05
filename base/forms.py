from django import forms
from django.contrib.auth.forms import (
        UserCreationForm,
        UserChangeForm,
        AuthenticationForm
)
from .models import CustomUser, PointTransaction, RedeemAward
from django.forms import ModelForm
from django.db.models import Sum


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
    description = forms.CharField(
        label='Description',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-sm',
                'placeholder': 'Reason for awarding the point'}
        ),
    )

    class Meta:
        model = PointTransaction
        fields = ['student', 'category', 'description']


class CustomAuthenticationForm(AuthenticationForm):
    """ authentication form """
    
    '''class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'class': 'fa fa-user', 'placeholder': 'USERNAME'}),
        }'''


class ReedemForm(forms.ModelForm):
    """ point award form """

    class Meta:
        model = RedeemAward
        fields = ['select_award']

        '''widgets = {
            'select_award': forms.Select(attrs={'class': 'form-control'}),
        }'''


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['select_award'].empty_label = 'Check available awards'


    def clean(self):
        cleaned_data = super().clean()

        if self.request:
            student = self.request.user
            total_points = (
                PointTransaction.objects.filter(student=student)
                .aggregate(Sum('category__point'))['category__point__sum'] or 0
            )
            total_redeemed = (
                RedeemAward.objects.filter(student=student)
                .aggregate(Sum('select_award__points'))
                .get('select_award__points__sum', 0) or 0
            )
            available_points = total_points - total_redeemed

            if available_points < cleaned_data.get('select_award').points:
                raise forms.ValidationError(
                        'Not enough points to redeem the award.'
                )

            cleaned_data['student'] = student

        return cleaned_data
