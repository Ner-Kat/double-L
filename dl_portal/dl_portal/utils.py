import os.path
import string
import random
from hashlib import sha256

from django.utils import timezone


def gen_random_word(length=12):
    symbols = string.ascii_letters + "".join(map(str, [i for i in range(10)]))
    return "".join(random.choice(symbols) for i in range(length))


def get_cke_filename(filename, request):
    now = timezone.now()

    path = ""

    name_data = [now.year, now.month, now.day, now.hour, now.minute, now.second, filename]
    new_name = "-".join(map(str, name_data)) + "-" + gen_random_word()
    new_name = sha256(new_name.encode('utf-8')).hexdigest()

    return path + new_name + os.path.splitext(filename)[1]
