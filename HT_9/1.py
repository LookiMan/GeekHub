"""

Перепишіть програму-банкомат на використання бази даних для збереження всих даних.
Використовувати БД sqlite3 та натівний Python.
Дока з прикладами: https://docs.python.org/3/library/sqlite3.html
Туторіал (один із): https://www.sqlitetutorial.net/sqlite-python/
Для уніфікації перевірки, в базі повинні бути 3 користувача:
  ім'я: user1, пароль: user1
  ім'я: user2, пароль: user2
  ім'я: admin, пароль: admin (у цього коритувача - права інкасатора)


python -m pip install -r requirements.txt

python3 -m pip install -r requirements.txt

"""

import getpass
from collections.abc import Callable
from typing import Optional
from colorama import init, Fore

import utils


init(autoreset=True)


_SESSION = {}


def set_user_id_form_session(username) -> None:
    _SESSION["user_id"] = username


def get_user_id_form_session() -> int:
    username = _SESSION.get("user_id")

    if username:
        return username
    else:
        raise ValueError("Id користувава не встановлено в сессії")


def test_system() -> None:
    try:
        utils.check_system()
    except Exception as exc:
        utils.logger.error(exc)
        exit(1)


def safe_input(prompt: str, validator: Callable) -> str:
    print(Fore.CYAN + "[>] ================")
    while True:
        raw_input = input(Fore.CYAN + f"{prompt}: ").strip()

        try:
            if not validator(raw_input):
                raise Exception()
        except:
            print(Fore.RED + "[!] введіть корректне значення")
        else:
            return raw_input


def post_menu(function: Callable) -> Callable:
    def menu_wrapper() -> None:
        function()

        print(Fore.YELLOW + "[>] ==================")
        print(Fore.YELLOW + "[1] Породовжити роботу")
        print(Fore.YELLOW + "[2] Вихід")
        command = safe_input("[<] введіть число", lambda v: int(v) in (1, 2))

        if command == "1":
            main_screen()
        elif command == "2":
            close_session()

    return menu_wrapper


@post_menu
def balance_view_screen() -> None:
    user_id = get_user_id_form_session()
    balance = utils.load_user_balance(user_id)
    print(Fore.GREEN + "[>] ==================")
    print(Fore.GREEN + f"[>] Ваш баланс: {balance}")
    utils.append_user_transactions(user_id, f"переглянув баланс. Баланс: {balance}")


@post_menu
def balance_replenishment_screen() -> None:
    user_id = get_user_id_form_session()
    balance = int(utils.load_user_balance(user_id))
    contribution = int(safe_input("[<] сума внесення", int))

    if contribution < 1:
        print(Fore.RED + f"[!] Сума внесення повинна бути більша за нуль")
    else:
        balance += contribution

        utils.save_user_balance(user_id, balance)
        utils.append_user_transactions(
            user_id, f"внесення коштів. Сума внесення {contribution}"
        )


@post_menu
def balance_withdraw_screen() -> None:
    user_id = get_user_id_form_session()
    balance = utils.load_user_balance(user_id)
    withdraw = int(safe_input("[<] сума для зняття", int))

    if withdraw > balance:
        print(Fore.RED + "[!] сума для зняття не може перевищувати суму на балансі")
    elif withdraw < 0:
        print(Fore.RED + "[!] сума для зняття не може бути меншою за нуль")
    else:
        balance -= withdraw

        avalible_banknotes = utils.load_banknotes()
        status, banknotes = utils.decomposer(withdraw, avalible_banknotes)

        if status == utils.DECOMPOSER_STATUSES["success"]:
            print(Fore.GREEN + "[>] " + utils.convert_dict_to_string(banknotes))
        else:
            print(Fore.RED + "[!] Неможливо видати вказану суму")

        utils.reduce_availble_banknotes(banknotes, avalible_banknotes)
        utils.save_banknotes(avalible_banknotes)
        utils.save_user_balance(user_id, balance)
        utils.append_user_transactions(user_id, f"зняття коштів. Сумма: {withdraw}")


@post_menu
def banknote_view_screen() -> None:
    avalible_banknotes = utils.load_banknotes()
    output = utils.convert_dict_to_string(avalible_banknotes)

    print(Fore.GREEN + "[>] Список банкнот:")
    print(Fore.GREEN + "[>]", Fore.GREEN + output)


@post_menu
def banknote_replenishment_screen() -> None:
    avalible_banknotes = utils.load_banknotes()
    nominals = list(avalible_banknotes.keys())

    print(Fore.GREEN + "[>] Номінали які використловуються:")
    print(Fore.GREEN + "[>]", Fore.GREEN + ", ".join(nominals))

    nominal = safe_input(
        "[>] вкажіть номінал для поповнення", lambda inp: inp in nominals
    )
    amount = safe_input(
        "[>] вкажіть кількість банкнот", lambda inp: int(inp) in range(1, 1000)
    )

    utils.increase_availble_banknotes({nominal: int(amount)}, avalible_banknotes)
    utils.save_banknotes(avalible_banknotes)


@post_menu
def collection_screen() -> None:
    print(Fore.YELLOW + "[>] ================")
    print(Fore.YELLOW + "[1] Перегляд банкнот")
    print(Fore.YELLOW + "[2] Внесення банкнот")
    print(Fore.YELLOW + "[3] Назад")
    print(Fore.YELLOW + "[4] Вихід")

    command = safe_input("[<] введіть число", lambda v: int(v) in range(1, 5))

    if command == "1":
        banknote_view_screen()
    elif command == "2":
        banknote_replenishment_screen()
    elif command == "3":
        main_screen()
    elif command == "4":
        close_session()
    else:
        main_screen()


def login_screen() -> Optional[str]:
    print(Fore.CYAN + f"[>] ================")

    username = input(Fore.CYAN + "[<] ім'я користувача: ").strip()
    password = getpass.getpass(prompt=Fore.CYAN + "[<] пароль: ").strip()

    user_id = utils.is_user_exists(username, password)
    if user_id:
        return user_id
    else:
        print(Fore.RED + "[!] Логін або пароль введено неправильно ")


def main_screen() -> None:
    user_id = get_user_id_form_session()

    if utils.is_incasator(user_id):
        service_screen()
    else:
        user_screen()


def user_screen() -> None:
    print(Fore.YELLOW + "[>] ================")
    print(Fore.YELLOW + "[1] Перегляд балансу")
    print(Fore.YELLOW + "[2] Поповнити баланс")
    print(Fore.YELLOW + "[3] Зняти готівку")
    print(Fore.YELLOW + "[4] Вихід")

    command = safe_input("[<] введіть число", lambda v: int(v) in range(1, 5))

    if command == "1":
        balance_view_screen()
    elif command == "2":
        balance_replenishment_screen()
    elif command == "3":
        balance_withdraw_screen()
    elif command == "4":
        close_session()
    else:
        main_screen()


def service_screen() -> None:
    print(Fore.YELLOW + "[>] ================")
    print(Fore.YELLOW + "[1] Перегляд балансу")
    print(Fore.YELLOW + "[2] Поповнити баланс")
    print(Fore.YELLOW + "[3] Зняти готівку")
    print(Fore.YELLOW + "[4] Інкасація")
    print(Fore.YELLOW + "[5] Вихід")

    command = safe_input("[<] введіть число", lambda v: int(v) in range(1, 6))

    if command == "1":
        balance_view_screen()
    elif command == "2":
        balance_replenishment_screen()
    elif command == "3":
        balance_withdraw_screen()
    elif command == "4":
        collection_screen()
    elif command == "5":
        close_session()
    else:
        main_screen()


def close_session() -> None:
    print(Fore.GREEN + "[>] Бувай!")
    exit(0)


def start() -> None:
    test_system()

    for attempt in range(3, 0, -1):
        user_id = login_screen()

        if user_id:
            set_user_id_form_session(user_id)
            main_screen()
        else:
            print(Fore.YELLOW + f"[i] Залишилось спроб: {attempt-1}")

    close_session()


def main() -> None:
    start()


if __name__ == "__main__":
    main()
