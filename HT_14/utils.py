import os
import logging
from collections.abc import Callable
from typing import Optional, Union

from requests import get
from colorama import init, Fore

from models import DecomposerStatuses


init(autoreset=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("./log.txt", "a", "utf-8")
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(name)s]: %(message)s", datefmt="%m/%d/%Y %I:%M:%S"
    )
)

logger.addHandler(handler)

root = "./src/"

PATHS = {
    "system": os.path.join(root, "system/"),
    "system_file": os.path.join(root, "system/%s"),
}

decomposer_statuses = DecomposerStatuses(success=1, fail=2)


def safe_input(
    prompt: str, *, validator: Callable, post_processor: Optional[Callable] = None
) -> Union[str, int]:
    print(Fore.CYAN + "[>] ================")
    while True:
        raw_input = input(Fore.CYAN + f"{prompt}: ").strip()

        try:
            if not validator(raw_input):
                raise Exception()
        except:
            print(Fore.RED + "[!] введіть корректне значення")
        else:
            if post_processor:
                return post_processor(raw_input)
            else:
                return raw_input


def get_path(path_name: str, *args) -> str:
    path = PATHS.get(path_name)

    if path:
        return path % args if args else path
    else:
        message = "Шлях під назвою '{path_name}' не зареєстровано в словарі PATHS"

        logger.error(message)
        raise FileNotFoundError(message)


def select_avalible_nominals(avalible_banknotes: dict) -> list:
    return list(
        [nominal for nominal in avalible_banknotes if avalible_banknotes[nominal] > 0]
    )


def reduce_availble_banknotes(banknotes_seized: dict, avalible_banknotes: dict) -> None:
    for nominal, amount in banknotes_seized.items():
        avalible_banknotes[nominal] -= amount


def increase_availble_banknotes(
    banknotes_added: dict, avalible_banknotes: dict
) -> None:

    for nominal, amount in banknotes_added.items():
        avalible_banknotes[nominal] += amount


def decomposer(total_sum: int, banknotes: dict) -> tuple:
    avalible_nominals = select_avalible_nominals(banknotes)

    result = {}

    for nominal in avalible_nominals:
        for _ in range(banknotes[nominal]):

            if total_sum < int(nominal):
                break

            status, _ = decomposer(total_sum % int(nominal), banknotes)

            if status == decomposer_statuses.success:
                total_sum -= int(nominal)

                if nominal not in result:
                    result[nominal] = 1
                else:
                    result[nominal] += 1

    if total_sum == 0:
        status = decomposer_statuses.success
    else:
        status = decomposer_statuses.fail

    return status, result


def convert_dict_to_string(data: dict, separator: str = ":") -> str:
    string: str = str()

    for key, value in data.items():
        string += f"{key}{separator}{value} "

    return string


def make_exchange_currency_request(params: dict) -> dict:
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange"

    responce = get(url, params=params)

    if responce.status_code == 200:
        return responce.json()
    else:
        return dict()
