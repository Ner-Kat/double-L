from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):
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
