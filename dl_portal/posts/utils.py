import os.path
from django.utils import timezone
from hashlib import sha256


# Миксин, заменяющий label_suffix для форм, связанных с моделью
class LabelSuffixMixin:
    def __init__(self, *args, **kwargs):
        if 'label_suffix' not in kwargs:
            kwargs['label_suffix'] = ''
        super(LabelSuffixMixin, self).__init__(*args, **kwargs)


def preview_upload_path(instance, filename):
    user = instance
    now = timezone.now()

    path = "{0}/{1}/{2}/".format(now.year, now.month, now.day)

    name_data = [user.id, user.username, now.year, now.month, now.day, now.hour, now.minute, now.second, filename]
    new_name = "-".join(map(str, name_data))
    new_name = sha256(new_name.encode('utf-8')).hexdigest()

    return "posts/previews/" + path + new_name + os.path.splitext(filename)[1]


# def strip_unshort_tags(value):
#     value = str(value)
#     while '<' in value and '>' in value:
#         new_value = _strip_once(value)
#         if value.count('<') == new_value.count('<'):
#             break
#         value = new_value
#     return value
