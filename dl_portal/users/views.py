from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, CreateView, DetailView, View

from .models import User
from .forms import RegistrationForm, LoginForm
from .utils import UserContextMixin


class Login(UserContextMixin, FormView):
    """
    Контроллер (view) аутентификации.
    """
    template_name = 'users/login.html'
    form_class = LoginForm

    def get_context(self):
        return {
            'title': 'Авторизация',
            'login_next': self.request.path_info,
        }

    def get_reflected_context(self, form):
        return {
            'form': form if form else self.form_class,
            **self.get_context()
        }

    def get_context_data(self, **kwargs):
        context = {
            **self.get_context(),
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            user.last_login = timezone.now()
            user.save()
            messages.add_message(request, messages.INFO, 'Вы успешно вошли!')
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('home')

        form = LoginForm(request.POST)
        messages.add_message(request, messages.ERROR, 'Неверное имя пользователя или пароль.')
        return render(request, self.template_name, self.get_reflected_context(form))


class Logout(View):
    """
    Контроллер (view) выхода из сессии
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.request.META.get('HTTP_REFERER'))


class Registration(UserContextMixin, CreateView):
    """
    Контроллер (view) регистрации.
    """
    template_name = 'users/registration.html'
    form_class = RegistrationForm

    def get_context(self):
        return {
            'title': 'Регистрация',
            'login_next': self.request.path_info,
        }

    def get_reflected_context(self, form):
        return {
            'form': form if form else self.form_class,
            **self.get_context()
        }

    def get_context_data(self, **kwargs):
        context = {
            **self.get_context(),
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }
        return context

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(request, messages.INFO, 'Вы успешно зарегистрировались!')
            return redirect(user.get_absolute_url())
        else:
            messages.add_message(request, messages.ERROR, 'Регистрация не была произведена.')
            return render(request, self.template_name, self.get_reflected_context(form))


class UserProfile(UserContextMixin, DetailView):
    """
    Контроллер (view) профиля пользователя.
    """
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'
    slug_url_kwarg = "username"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = {
            **self.get_user_context(),
            **super(UserProfile, self).get_context_data()
        }
        context_adding = {
            'title': context['user'].nickname,
            'login_next': self.request.path_info,
        }

        return {**context, **context_adding}
