from datetime import datetime
import threading
import pytz


CHOICES = (
    (0, "newstories"),
    (1, "showstories"),
    (2, "askstories"),
    (3, "jobstories"),
)


def ctime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=pytz.UTC)


def Thread(function):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(
            target=function, daemon=True, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper
