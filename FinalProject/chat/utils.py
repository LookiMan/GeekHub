import logging
from typing import Callable

from django.conf import settings


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("./logs.txt", "a", "utf-8")
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(name)s]: %(message)s", datefmt="%m/%d/%Y %I:%M:%S"
    )
)

logger.addHandler(handler)
