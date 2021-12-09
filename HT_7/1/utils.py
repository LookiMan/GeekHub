import os
import csv
import json
import hashlib
from datetime import datetime


def create_password_hash(string):
    bytes_data = string.encode()
    solt = 'solt1234'.encode()
    sha256 = hashlib.sha256(bytes_data)

    for _ in range(1000):
        sha256.update(sha256.digest()+bytes_data+solt)

    return sha256.hexdigest()


def get_users():
    with open('./users/users.data', newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        return [item for item in reader]


def load_user_balance(username):
    with open(f'./balances/{username}_balance.data') as file:
        return file.read()


def save_user_balance(username, balance):
    with open(f'./balances/{username}_balance.data', mode='w') as file:
        file.write(balance)


def load_user_transactions(username):
    with open(f'./transactions/{username}_transactons.data') as file:
        return json.load(file)


def save_user_transactions(username, data):
    with open(f'./transactions/{username}_transactons.data', mode='r+') as file:
        json.dump(data, file, indent=4)


def append_user_transactions(username, transaction):
    transactions = load_user_transactions(username)
    transactions[str(datetime.now())] = transaction
    save_user_transactions(username, transactions)


def time():
    return str(datetime.now())


def check_system_files(fp):
    error_flag = False

    for directory in ('./users', './balances', './transactions'):
        if not os.path.exists(directory):
            print(f'{time()}: Відсутня директорія {directory}', file=fp)
            error_flag = True

    for username, _ in get_users():
        if not os.path.exists(f'./balances/{username}_balance.data'):
            print(f'{time()}: Відсутній файл балансу користувача {username}', file=fp)
            error_flag = True

        if not os.path.exists(f'./transactions/{username}_transactons.data'):
            print(
                f'{time()}: Відсутній файл транзакцій користувача {username}', file=fp)
            error_flag = True

    if error_flag:
        raise Exception('Виявлено критичну помилку')
    else:
        print(f'{time()}: Перевірка успішна', file=fp)
