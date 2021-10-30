from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", }),
                                       label='Подтверждение пароля', )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Логин",
            }),
            'email': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "example@domain",
            }),
            'password': forms.PasswordInput(attrs={
                "class": "form-control",
            }),
        }

        labels = {
            'username': "Имя пользователя",
            'email': "E-mail",
            'password': "Пароль",
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    def clean(self):
        super(RegistrationForm, self).clean()

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if not password == password_confirm:
            self.add_error('password_confirm', 'Пароли не совпадают')
            raise ValidationError("Пароли не совпадают")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Логин",
            }),
            'password': forms.PasswordInput(attrs={
                "class": "form-control",
            }),
        }

        labels = {
            'username': "Имя пользователя",
            'password': "Пароль",
        }
