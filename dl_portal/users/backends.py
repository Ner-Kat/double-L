from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


class UsersAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        users = settings.AUTH_USER_MODEL

        try:
            user = users.objeects.get(username=username)
        except ObjectDoesNotExist:
            try:
                user = users.objects.get(email=username)
            except ObjectDoesNotExist:
                return None
            return None

        valid_pass = check_password(password, user.password)
        if valid_pass:
            return user

        return None

    def get_user(self, user_id):
        try:
            return settings.AUTH_USER_MODEL.objects.get(pk=user_id)
        except settings.AUTH_USER_MODEL.DoesNotExist:
            return None
