"""
1. Програма-банкомат.
   Створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) та історію транзакцій (файл <{username}_transactions.data>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено число; знімається не більше, ніж є на рахунку).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - спочатку - логін користувача - програма запитує ім'я/пароль. Якщо вони неправильні - вивести повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
      - потім - елементарне меню типа:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив :)

login: Ivan   password: 1111
login: John   password: 2222
login: Smith  password: 0000
login: Adam   password: 4444
login: Maria  password: 7777



python -m pip install -r requirements.txt

python3 -m pip install -r requirements.txt

"""

import getpass

from colorama import init, Fore

import utils


init(autoreset=True)

_USERNAME = ''


def get_current_username():
    return _USERNAME


def set_current_username(username):

    _USERNAME


def test_system():
    fp = open('./log.txt', 'a')

    try:
        utils.check_system_files(fp)
    except Exception as exc:
        print(Fore.RED + f'[!] {exc}')
        exit(1)
    finally:
        fp.close()


def safe_input(prompt, validator):
    print(Fore.CYAN + '[>] ================')
    while True:
        raw_input = input(Fore.CYAN + f'{prompt}: ').strip()

        try:
            if not validator(raw_input):
                raise Exception()
        except:
            print(Fore.RED + '[!] введіть корректне значення')
        else:
            return raw_input


def sub_menu(username):
    print(Fore.YELLOW + '[>] ==================')
    print(Fore.YELLOW + '[1] Породовжити роботу')
    print(Fore.YELLOW + '[2] вихід')
    command = safe_input('[<] введіть число', lambda v: int(v) in (1, 2))

    if command == '1':
        main_screen(username)
    elif command == '2':
        close_session()


def balance_view_screen(username):
    balance = utils.load_user_balance(username)
    print(Fore.GREEN + '[>] ==================')
    print(Fore.GREEN + f'[>] Ваш баланс: {balance}')
    utils.append_user_transactions(username, ('переглянув баланс', balance))


def balance_replenishment_screen(username):
    balance = int(utils.load_user_balance(username))
    contribution = int(safe_input('[<] сума внесення', int))

    if contribution < 1:
        print(Fore.RED + f'[!] Сума внесення повинна бути більша за нуль')
    else:
        balance += contribution

        utils.save_user_balance(username, str(balance))
        utils.append_user_transactions(
            username, ('внесення коштів', contribution))


def balance_withdraw_screen(username):
    balance = int(utils.load_user_balance(username))
    withdraw = int(safe_input('[<] сума для зняття', int))

    if withdraw > balance:
        print(
            Fore.RED + '[!] сума для зняття не може перевищувати суму на балансі')
    elif withdraw < 0:
        print(
            Fore.RED + '[!] сума для зняття не може бути меншою за нуль')
    else:
        balance -= withdraw

    utils.save_user_balance(username, str(balance))
    utils.append_user_transactions(username, ('зняття коштів', withdraw))


def login_screen():
    print(Fore.CYAN + f'[>] ================')

    username = input(Fore.CYAN + '[<] ім\'я користувача: ').strip()
    password = getpass.getpass(prompt=Fore.CYAN + '[<] пароль: ').strip()

    if [username, utils.create_password_hash(password)] in utils.get_users():
        return username
    else:
        print(Fore.RED + '[!] Логін або пароль введено неправильно ')


def main_screen(username):
    print(Fore.YELLOW + '[>] ================')
    print(Fore.YELLOW + '[1] Перегляд балансу')
    print(Fore.YELLOW + '[2] Поповнити баланс')
    print(Fore.YELLOW + '[3] Зняти готівку')
    print(Fore.YELLOW + '[4] вихід')

    command = safe_input('[<] введіть число', lambda v: int(v) in range(1, 5))

    if command == '1':
        balance_view_screen(username)
        sub_menu(username)
    elif command == '2':
        balance_replenishment_screen(username)
        sub_menu(username)
    elif command == '3':
        balance_withdraw_screen(username)
        sub_menu(username)
    elif command == '4':
        close_session()
    else:
        main_screen(username)


def close_session():
    print('[>] Бувай!')
    exit(0)


def start():
    test_system()

    for i in range(3):
        username = login_screen()

        if username:
            main_screen(username)
        else:
            print(Fore.YELLOW + f'[i] Залишилось спроб: {2-i}')
            close_session()


def main():
    start()


if __name__ == '__main__':
    main()
