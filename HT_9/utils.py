import os
import csv
import json
import hashlib
import logging
from datetime import datetime
from typing import Union, Tuple, Any

import database

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler("./log.txt", "a", "utf-8")
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(name)s]: %(message)s", datefmt="%m/%d/%Y %I:%M:%S"
    )
)

logger.addHandler(handler)

db = database.SQLiteDatabase("./src/system/db.sqlite3")


DECOMPOSER_STATUSES = {
    "success": 1,
    "fail": 2,
}

root = "./src/"

PATHS = {
    "system": os.path.join(root, "system/"),
    "balances": os.path.join(root, "balances/"),
    "transactions": os.path.join(root, "transactions/"),
    "system_file": os.path.join(root, "system/%s"),
    "user_balances": os.path.join(root, "balances/%s_balance.data"),
    "user_transactions": os.path.join(root, "transactions/%s_transactons.data"),
    "users": os.path.join(root, "system/users.data"),
    "banknotes": os.path.join(root, "system/banknotes.json"),
}


def get_path(path_name: str, *args) -> str:
    path = PATHS.get(path_name)

    if path:
        return path % args if args else path
    else:
        message = "Шлях під назвою '{path_name}' не зареєстровано в словарі PATHS"

        logger.error(message)
        raise FileNotFoundError(message)


def load_banknotes() -> dict:
    banknotes = {}

    for item in db.select_banknotes():
        banknotes[item[0]] = item[1]

    return banknotes


def save_banknotes(banknotes: dict) -> None:
    db.update_banknotes(banknotes)


def load_user_balance(user_id: int) -> dict:
    return db.select_user_balance(user_id)


def save_user_balance(user_id: int, balance: int) -> None:
    db.update_user_balance(user_id, balance)


def append_user_transactions(user_id: str, transaction: str) -> None:
    db.append_user_transaction(user_id, transaction)


def check_directories(directories: Union[list, tuple]) -> bool:
    error_flag = False

    for directory in directories:
        if not os.path.exists(get_path(directory)):
            logger.error("Відсутня директорія '%s'" % directory)

            error_flag = True

    return error_flag


def check_files(files: Union[list, tuple]) -> bool:
    error_flag = False

    for filename in files:
        if not os.path.exists(filename):
            logger.error("Відсутній файл '%s'" % filename)

            error_flag = True

    return error_flag


def check_system_directories() -> bool:
    return check_directories(("system",))


def check_system_files() -> bool:
    filenames = []

    for directory in ("system_file",):
        for filename in ("db.sqlite3",):
            filenames.append(get_path(directory, filename))

    return check_files(filenames)


def check_system() -> None:
    logger.info("Початок перевірки...")

    errors = [
        check_system_directories(),
        check_system_files(),
    ]

    if any(errors):
        logger.error("Завершення програми через критичну помилку")
        raise Exception("Виявлено критичну помилку")
    else:
        logger.info("Перевірка пройшла успішно")


def select_avalible_nominals(avalible_banknotes: dict) -> list:
    return list(
        [nominal for nominal in avalible_banknotes if avalible_banknotes[nominal] > 0]
    )


def reduce_availble_banknotes(banknotes_seized: dict, avalible_banknotes: dict) -> None:
    for banknote in banknotes_seized:
        avalible_banknotes[banknote] -= banknotes_seized[banknote]


def increase_availble_banknotes(
    banknotes_seized: dict, avalible_banknotes: dict
) -> None:
    for banknote in banknotes_seized:
        avalible_banknotes[banknote] += banknotes_seized[banknote]


def decomposer(total_sum: int, banknotes: dict) -> tuple:
    avalible_nominals = select_avalible_nominals(banknotes)

    result = {}

    for nominal in avalible_nominals:
        for _ in range(banknotes[nominal]):

            if total_sum < int(nominal):
                break

            status, _ = decomposer(total_sum % int(nominal), banknotes)

            if status == DECOMPOSER_STATUSES["success"]:
                total_sum -= int(nominal)

                if nominal not in result:
                    result[nominal] = 1
                else:
                    result[nominal] += 1

    status = (
        DECOMPOSER_STATUSES["success"]
        if total_sum == 0
        else DECOMPOSER_STATUSES["fail"]
    )

    return status, result


def convert_dict_to_string(data: dict, separator: str = ":") -> str:
    string: str = str()

    for key, value in data.items():
        string += f"{key}{separator}{value} "

    return string


def is_incasator(user_id: int) -> bool:
    return db.is_incasator(user_id)


def is_user_exists(username: str, password: str) -> bool:
    return db.is_user_exists(username, password)
