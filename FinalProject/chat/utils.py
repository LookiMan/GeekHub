from datetime import datetime

import logging
import pytz


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("./logs.txt", "a", "utf-8")
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(name)s]: %(message)s", datefmt="%m/%d/%Y %I:%M:%S"
    )
)

logger.addHandler(handler)


def ctime(timestamp):
    return datetime.fromtimestamp(timestamp, tz=pytz.UTC)


def generator(content):
    chunk_size = 4096

    content.seek(0)
    while True:
        chunk = content.read(chunk_size)
        if not chunk:
            return None
        yield chunk
