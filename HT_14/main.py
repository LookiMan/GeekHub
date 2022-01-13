"""

Домашнє завдання №14: Переписати останню версію банкомата з використанням ООП.


python -m pip install -r requirements.txt

python3 -m pip install -r requirements.txt

"""

import getpass
from collections.abc import Callable
from typing import Union, Dict
from colorama import init, Fore

import utils
import db
import models
import storage
import system_test


init(autoreset=True)


class ATM(object):
    def __init__(self, storage: storage.Storage, system_test_utility: system_test.SystemTest) -> None:
        self.session: Dict[str, Union[models.User, models.Incasator]] = {}
        self.storage = storage
        self.system_test_utility = system_test_utility

    def set_user_form_session(self, user: Union[models.User, models.Incasator]) -> None:
        self.session["user"] = user

    def get_user_form_session(self) -> Union[models.User, models.Incasator]:
        user = self.session.get("user")

        if user:
            return user
        else:
            raise ValueError("Користувача не встановлено в сессії")

    def post_menu(function: Callable) -> Callable:
        def menu_wrapper(self, *args, **kwargs) -> None:
            function(self, *args, **kwargs)

            print(Fore.YELLOW + "[>] ==================")
            print(Fore.YELLOW + "[1] Породовжити роботу")
            print(Fore.YELLOW + "[2] Вихід")
            command = utils.safe_input("[<] введіть число",
                                       validator=lambda v: int(v) in (1, 2))

            if command == "1":
                self.main_screen()
            elif command == "2":
                self.close_session()

        return menu_wrapper

    @post_menu
    def balance_view_screen(self) -> None:
        user = self.get_user_form_session()
        balance = user.balance()
        print(Fore.GREEN + "[>] ==================")
        print(Fore.GREEN + f"[>] Ваш баланс: {balance}")
        user.append_user_transaction(f"Переглянув баланс. Баланс: {balance}")

    @post_menu
    def balance_replenishment_screen(self) -> None:
        user = self.get_user_form_session()
        balance = user.balance()
        contribution = utils.safe_input(
            "[<] сума внесення", validator=int, post_processor=int)

        if contribution < 1:
            print(Fore.RED + f"[!] Сума внесення повинна бути більша за нуль")
        else:
            balance += contribution

            user.save_balance(balance)
            user.append_user_transaction(
                f"Внесення коштів. Сума:{contribution}")

    @post_menu
    def balance_withdraw_screen(self) -> None:
        user = self.get_user_form_session()
        balance = user.balance()
        withdraw = utils.safe_input("[<] сума для зняття",
                                    validator=int, post_processor=int)

        if withdraw > balance:
            print(
                Fore.RED + "[!] сума для зняття не може перевищувати суму на балансі")
        elif withdraw < 0:
            print(Fore.RED + "[!] сума для зняття не може бути меншою за нуль")
        else:
            balance -= withdraw

            avalible_banknotes = self.storage.load_banknotes()
            status, banknotes = utils.decomposer(withdraw, avalible_banknotes)

            if status == utils.decomposer_statuses.success:
                print(Fore.GREEN + "[>] " +
                      utils.convert_dict_to_string(banknotes))
            else:
                print(Fore.RED + "[!] Неможливо видати вказану суму")

            utils.reduce_availble_banknotes(banknotes, avalible_banknotes)
            self.storage.save_banknotes(avalible_banknotes)
            #
            user.save_balance(balance)
            user.append_user_transaction(f"Зняття коштів. Сумма: {withdraw}")

    @post_menu
    def banknote_view_screen(self) -> None:
        avalible_banknotes = self.storage.load_banknotes()
        output = utils.convert_dict_to_string(avalible_banknotes)

        print(Fore.GREEN + "[>] Список банкнот:")
        print(Fore.GREEN + "[>]", Fore.GREEN + output)

    @post_menu
    def banknote_replenishment_screen(self) -> None:
        avalible_banknotes = self.storage.load_banknotes()
        nominals = list(avalible_banknotes.keys())

        print(Fore.GREEN + "[>] Номінали які використловуються:")
        print(Fore.GREEN + "[>]", Fore.GREEN + ", ".join(nominals))

        nominal = utils.safe_input(
            "[>] вкажіть номінал для поповнення",
            validator=lambda inp: inp in nominals,
        )

        amount = utils.safe_input(
            "[>] вкажіть кількість банкнот",
            validator=lambda inp: int(inp) in range(1, 1000),
            post_processor=int,
        )

        utils.increase_availble_banknotes(
            {nominal: amount}, avalible_banknotes)

        self.storage.save_banknotes(avalible_banknotes)

    @post_menu
    def currency_courses(self):
        exchange_courses = utils.make_exchange_currency_request({"coursid": 5})

        if exchange_courses:
            for cours in exchange_courses:
                print(Fore.GREEN + f"[>] {cours['ccy']} \ {cours['base_ccy']}")
                print(Fore.GREEN + f"[>] купівля:\t{cours['buy']}")
                print(Fore.GREEN + f"[>] продаж:\t{cours['sale']}")
        else:
            print(Fore.RED + "[!] Неможливо отримати курси обміну валют")

    @post_menu
    def collection_screen(self) -> None:
        print(Fore.YELLOW + "[>] ================")
        print(Fore.YELLOW + "[1] Перегляд банкнот")
        print(Fore.YELLOW + "[2] Внесення банкнот")
        print(Fore.YELLOW + "[3] Назад")
        print(Fore.YELLOW + "[4] Вихід")

        command = utils.safe_input("[<] введіть число",
                                   validator=lambda v: int(v) in range(1, 5))

        if command == "1":
            self.banknote_view_screen()
        elif command == "2":
            self.banknote_replenishment_screen()
        elif command == "3":
            self.main_screen()
        elif command == "4":
            self.close_session()
        else:
            self.main_screen()

    def login_screen(self) -> Union[models.User, models.Incasator, None]:
        print(Fore.CYAN + f"[>] ================")

        username = input(Fore.CYAN + "[<] ім'я користувача: ").strip()
        password = getpass.getpass(prompt=Fore.CYAN + "[<] пароль: ").strip()

        user_id = self.storage.is_user_exists(username, password)

        if user_id:
            if self.storage.is_incasator(user_id):
                return models.Incasator(user_id, username, self.storage)
            else:
                return models.User(user_id, username, self.storage)
        else:
            print(Fore.RED + "[!] Логін або пароль введено неправильно ")

    def main_screen(self) -> None:
        user = self.get_user_form_session()

        if user.is_incasator():
            self.service_screen()
        else:
            self.user_screen()

    def user_screen(self) -> None:
        print(Fore.YELLOW + "[>] ================")
        print(Fore.YELLOW + "[1] Перегляд балансу")
        print(Fore.YELLOW + "[2] Поповнити баланс")
        print(Fore.YELLOW + "[3] Зняти готівку")
        print(Fore.YELLOW + "[4] Курси валют")
        print(Fore.YELLOW + "[5] Вихід")

        command = utils.safe_input("[<] введіть число",
                                   validator=lambda v: int(v) in range(1, 6))

        if command == "1":
            self.balance_view_screen()
        elif command == "2":
            self.balance_replenishment_screen()
        elif command == "3":
            self.balance_withdraw_screen()
        elif command == "4":
            self.currency_courses()
        elif command == "5":
            self.close_session()
        else:
            self.main_screen()

    def service_screen(self) -> None:
        print(Fore.YELLOW + "[>] ================")
        print(Fore.YELLOW + "[1] Перегляд балансу")
        print(Fore.YELLOW + "[2] Поповнити баланс")
        print(Fore.YELLOW + "[3] Зняти готівку")
        print(Fore.YELLOW + "[4] Курси валют")
        print(Fore.YELLOW + "[5] Інкасація")
        print(Fore.YELLOW + "[6] Вихід")

        command = utils.safe_input("[<] введіть число",
                                   validator=lambda v: int(v) in range(1, 7))

        if command == "1":
            self.balance_view_screen()
        elif command == "2":
            self.balance_replenishment_screen()
        elif command == "3":
            self.balance_withdraw_screen()
        elif command == "4":
            self.currency_courses()
        elif command == "5":
            self.collection_screen()
        elif command == "6":
            self.close_session()
        else:
            self.main_screen()

    def close_session(self) -> None:
        print(Fore.GREEN + "[>] Бувай!")
        exit(0)

    def system_test(self) -> None:
        try:
            self.system_test_utility.start()
        except Exception as exc:
            utils.logger.error(exc)
            exit(1)

    def start(self) -> None:
        self.system_test()

        for attempt in range(3, 0, -1):
            user = self.login_screen()

            if user:
                self.set_user_form_session(user)
                self.main_screen()
            else:
                print(Fore.YELLOW + f"[i] Залишилось спроб: {attempt-1}")

        self.close_session()


def main() -> None:
    tester = system_test.SystemTest(utils.logger)
    db_storage = storage.Storage(db.SQLite("./src/system/db.sqlite3"))

    atm = ATM(db_storage, tester)
    atm.start()


if __name__ == "__main__":
    main()
