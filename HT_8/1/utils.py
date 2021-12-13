import os
import csv
import json
import hashlib
import logging
from datetime import datetime
from typing import Union, Optional, Tuple, Any

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('./log.txt', 'a', 'utf-8')
handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(name)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S'))

logger.addHandler(handler)


DECOMPOSER_STATUSES = {
    'success': 1,
    'fail': 2,
}

root = './src/'

PATHS = {
    'system': os.path.join(root, 'system/'),
    'balances': os.path.join(root, 'balances/'),
    'transactions': os.path.join(root, 'transactions/'),
    'system_file': os.path.join(root, 'system/%s'),
    'user_balances': os.path.join(root, 'balances/%s_balance.data'),
    'user_transactions': os.path.join(root, 'transactions/%s_transactons.data'),
    'users': os.path.join(root, 'system/users.data'),
    'banknotes': os.path.join(root, 'system/banknotes.json'),
}


def get_path(path_name: str, *args) -> str:
    path = PATHS.get(path_name)

    if path:
        return path % args if args else path
    else:
        message = 'Шлях під назвою \'{path_name}\' не зареєстровано в словарі PATHS'

        logger.error(message)
        raise FileNotFoundError(message)


def create_password_hash(string: str) -> str:
    bytes_data = string.encode()
    solt = 'solt1234'.encode()
    sha256 = hashlib.sha256(bytes_data)

    for _ in range(1000):
        sha256.update(sha256.digest()+bytes_data+solt)

    return sha256.hexdigest()


def get_usernames() -> list:
    with open(get_path('users'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        return [row['username'] for row in reader]


def get_username_and_password() -> list:
    with open(get_path('users'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        return [[row['username'], row['password']] for row in reader]


def get_username_and_status() -> list:
    with open(get_path('users'), newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        return [[row['username'], row['is_collector']] for row in reader]


def load_banknotes() -> dict:
    with open(get_path('banknotes')) as file:
        return json.load(file)


def save_banknotes(banknotes: dict) -> None:
    with open(get_path('banknotes'), mode='w') as file:
        json.dump(banknotes, file, indent=4)


def load_user_balance(username: str) -> str:
    with open(get_path('user_balances', username)) as file:
        return file.read()


def save_user_balance(username: str, balance: str) -> None:
    with open(get_path('user_balances', username), mode='w') as file:
        file.write(balance)


def load_user_transactions(username: str) -> dict:
    with open(get_path('user_transactions', username)) as file:
        return json.load(file)


def save_user_transactions(username: str, data: dict) -> None:
    with open(get_path('user_transactions', username), mode='r+') as file:
        json.dump(data, file, indent=4)


def append_user_transactions(username: str, transaction: Tuple[Any, Any]) -> None:
    transactions = load_user_transactions(username)
    transactions[time()] = transaction
    save_user_transactions(username, transactions)


def time() -> str:
    return str(datetime.now())


def check_directories(directories: Union[list, tuple]) -> bool:
    error_flag = False

    for directory in directories:
        if not os.path.exists(get_path(directory)):
            logger.error('Відсутня директорія \'%s\'' % directory)

            error_flag = True

    return error_flag


def check_files(files: Union[list, tuple]) -> bool:
    error_flag = False

    for filename in files:
        if not os.path.exists(filename):
            logger.error('Відсутній файл \'%s\'' % filename)

            error_flag = True

    return error_flag


def check_system_directories() -> bool:
    return check_directories(('system',))


def check_system_files() -> bool:
    filenames = []

    for directory in ('system_file',):
        for filename in ('users.data', 'banknotes.json'):
            filenames.append(get_path(directory, filename))

    return check_files(filenames)


def check_users_directories() -> bool:
    return check_directories(('balances', 'transactions'))


def check_users_files() -> bool:
    filenames = []

    for username in get_usernames():
        for path_name in ('user_balances', 'user_transactions'):
            filenames.append(get_path(path_name, username))

    return check_files(filenames)


def check_system() -> None:
    logger.info('Початок перевірки...')

    errors = [
        check_system_directories(),
        check_system_files(),
        check_users_directories(),
        check_users_files(),
    ]

    if any(errors):
        logger.error('Завершення програми через критичну помилку')
        raise Exception('Виявлено критичну помилку')
    else:
        logger.info('Перевірка пройшла успішно')


def select_avalible_nominals(avalible_banknotes: dict) -> list:
    return list([nominal for nominal in avalible_banknotes if avalible_banknotes[nominal] > 0])


def reduce_availble_banknotes(banknotes_seized: dict, avalible_banknotes: dict) -> None:
    for banknote in banknotes_seized:
        avalible_banknotes[banknote] -= banknotes_seized[banknote]


def increase_availble_banknotes(banknotes_seized: dict, avalible_banknotes: dict) -> None:
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

            if status == DECOMPOSER_STATUSES['success']:
                total_sum -= int(nominal)

                if nominal not in result:
                    result[nominal] = 1
                else:
                    result[nominal] += 1

    status = DECOMPOSER_STATUSES['success'] if total_sum == 0 else DECOMPOSER_STATUSES['fail']

    return status, result


def convert_dict_to_string(data: dict, separator: str = ':') -> str:
    string: str = str()

    for key, value in data.items():
        string += f'{key}{separator}{value} '

    return string


def is_collector(current_username: str) -> bool:
    for username, status in get_username_and_status():
        if current_username == username and status == '1':
            return True
    return False


def is_exists(username: str, password: str) -> bool:
    return [username, create_password_hash(password)] in get_username_and_password()
