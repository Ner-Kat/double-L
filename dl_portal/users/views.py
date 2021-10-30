from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import FormView, CreateView, DetailView

from .models import User
from .forms import RegistrationForm, LoginForm


class Login(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_context(self):
        return {
            'title': 'Авторизация'
        }

    def get_reflected_context(self, form):
        return {
            'form': form if form else self.form_class,
            **self.get_context()
        }

    def get_context_data(self, **kwargs):
        context = {
            **self.get_context(),
            **super().get_context_data(**kwargs)
        }

        return context

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)


class Registration(CreateView):
    template_name = 'users/registration.html'
    form_class = RegistrationForm

    def get_context(self):
        return {
            'title': 'Регистрация',
        }

    def get_reflected_context(self, form):
        return {
            'form': form if form else self.form_class,
            **self.get_context()
        }

    def get_context_data(self, **kwargs):
        context = {
            **self.get_context(),
            **super().get_context_data(**kwargs)
        }
        return context

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Регистрация не была произведена.')
            return render(request, self.template_name, self.get_reflected_context(form))


class UserProfile(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'
