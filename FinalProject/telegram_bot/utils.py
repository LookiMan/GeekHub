import io
import os
import random
from datetime import datetime
import pytz

import PIL

from django.conf import settings


def save_user_image(content, filename):
    path = os.path.join(settings.PHOTOS_ROOT, filename)

    image = PIL.Image.open(io.BytesIO(content))
    image.save(path)

    return path


def save_file(content, filename):
    path = os.path.join(settings.MEDIA_ROOT, filename)

    with open(path, mode="wb") as file:
        file.write(content)

    return filename


def set_default_image():
    choices = (
        "default1.png",
        "default2.png",
        "default3.png",
        "default4.png",
        "default5.png",
        "default6.png"
    )

    return os.path.join("default", random.choice(choices))


def ctime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=pytz.UTC)
