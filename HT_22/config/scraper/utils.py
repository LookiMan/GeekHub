from datetime import datetime
import pytz


CHOICES = (
    (0, "newstories"),
    (1, "showstories"),
    (2, "askstories"),
    (3, "jobstories"),
)


def ctime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=pytz.UTC)
