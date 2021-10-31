from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

from .models import User


class UsersAuthBackend(BaseBackend):
    """
    Основной backend аутентификации на сайте.
    Позволяет аутентифицироваться по паре username-password или email-password.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.prefetch_related('groups', 'lore_groups').get(username=username)
        except ObjectDoesNotExist:
            try:
                user = User.objects.prefetch_related('groups', 'lore_groups').get(email=username)
            except ObjectDoesNotExist:
                return None
            return None

        valid_pass = check_password(password, user.password)
        if valid_pass:
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
