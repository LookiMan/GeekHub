import os
import random
from datetime import datetime
import pytz


def get_default_image():
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
