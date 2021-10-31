import os.path
from hashlib import sha256
from django.utils import timezone


class UserContextMixin:
    def get_user_context(self):
        user = self.request.user
        if user.is_authenticated:
            context = {
                'subj_id': user.pk,
                'subj_username': user.username,
                'subj_email': user.email,
                'subj_nickname': user.nickname,
                'subj_is_active': user.is_active,
                'subj_is_admin': user.is_admin,
                'subj_is_superadmin': user.is_superadmin,
                'subj_date_joined': user.date_joined,
                'subj_last_login': user.last_login,
                'subj_avatar': user.avatar,
                'subj_groups': user.get_groups_names_list(),
                'subj_lore_groups': user.get_lore_groups_names_list(),
            }
        else:
            context = {
                'subj_id': 0,
                'subj_username': '',
                'subj_nickname': '',
                'subj_is_admin': False,
                'subj_is_superadmin': False,
            }

        return context


def get_upload_path(instance, filename):
    user = instance
    now = timezone.now()

    path = "{0}/{1}/{2}/".format(now.year, now.month, now.day)

    name_data = [user.id, user.username, now.year, now.month, now.day, now.hour, now.minute, now.second, filename]
    new_name = "-".join(map(str, name_data))
    new_name = sha256(new_name.encode('utf-8')).hexdigest()

    return path + new_name + os.path.splitext(filename)[1]


def avatars_upload_path(instance, filename):
    return "u/avatars/" + get_upload_path(instance, filename)


def banners_upload_path(instance, filename):
    return "u/banners/" + get_upload_path(instance, filename)
