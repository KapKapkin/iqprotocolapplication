from allauth.account.forms import LoginForm, SignupForm
from datetime import datetime, timedelta
from django import forms

from eventrequests.models import AvWindow


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': "Введите email"})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'type': 'password', 'class': 'form-control', 'placeholder': "Введите пароль", 'id': "loginPassword"})


class UserSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': "Введите email"})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'type': 'password', 'class': 'form-control', 'placeholder': "Введите пароль", 'id': "loginPassword"})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'type': 'password', 'class': 'form-control', 'placeholder': "Подтвердите пароль", 'id': "loginPassword"})


class WindowForm(forms.ModelForm):
    place = forms.CharField(

        label="Место",
        widget=forms.Textarea(attrs={
            'class': 'form-application',
            'rows': 1,
            'cols': 30,
            'placeholder': "Введите место:"})
    )

    class Meta:
        model = AvWindow
        fields = ('date', 'time', 'place')
        labels = {
            'date': "Дата:",
            'time': "Время:",
            'place': "Место проведения церемонии (зал, павильон/корпус):",
        }

        widgets = {
            'date': forms.widgets.Input(attrs={
                'type': 'date',
                'class': 'form-application',
                'min': datetime.now().date() + timedelta(days=1)
            }),

            'time': forms.widgets.Input(attrs={
                'type': 'time',
                'class': 'form-application',
                'min': datetime.now().time()
            }),
        }
