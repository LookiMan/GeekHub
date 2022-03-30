import logging
import traceback
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


def action_logger(function: Callable) -> Callable:

    def wrapper(*args, **kwargs):
        action_logger = print if settings.DEBUG else logger

        action_logger(f"Starting function '{function}' execution...")
        try:
            result = function(*args, **kwargs)
        except Exception as exc:
            action_logger(
                f"In function '{function}' an exception occurred: {exc}")
            logger.exception('Got exception on main handler')
        else:
            action_logger(
                f"Function execution '{function}' finished successfully!"
            )

            return result

    return wrapper
