"""
2. Написати скрипт, який буде приймати від користувача назву валюти і початкову дату.
   - Перелік валют краще принтануть.
   - Також не забудьте указати, в якому форматі коритувач повинен ввести дату.
   - Додайте перевірку, чи введена дата не знаходиться у майбутньому ;)
   - Також перевірте, чи введена правильна валюта.
   Виконуючи запроси до API архіву курсу валют Приватбанку, вивести інформацію про зміну
   курсу обраної валюти (Нацбанк) від введеної дати до поточної. Приблизний вивід наступний:
   Currency: USD
   Date: 12.12.2021
   NBU:  27.1013   -------
   Date: 13.12.2021
   NBU:  27.0241   -0,0772
   Date: 14.12.2021
   NBU:  26.8846   -0,1395

P.S. Не забувайте про файл requirements.txt
P.P.S. Не треба сходу ДДОСить Приватбанк - додайте хоча б по 0.5 секунди між запросами.
       Хоч у них і не написано за троттлінг, але будьмо чемними ;)
Інформація для виконання:
- документація API Приватбанка:
  - архів курсів: https://api.privatbank.ua/#p24/exchangeArchive
  - поточний курс: https://api.privatbank.ua/#p24/exchange
- інформація про використання форматування дати в Python: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

"""

import typing
import time
from datetime import datetime, timedelta

import requests
from colorama import init, Fore

from task_1 import safe_input


init(autoreset=True)


def make_request(params: dict) -> dict:
    url = " https://api.privatbank.ua/p24api/exchange_rates?json"

    responce = requests.get(url, params=params)

    if responce.status_code == 200:
        return responce.json()
    else:
        return dict()


def date_range(
    start_date: datetime, end_date: datetime
) -> typing.Generator[str, None, None]:

    delta = timedelta(days=1)

    while start_date <= end_date:
        yield start_date.strftime("%d.%m.%Y")

        start_date += delta


def string_per_date(string: str) -> datetime:
    return datetime.strptime(string, "%d.%m.%Y")


def main() -> None:
    available_currencies = (
        "USD",
        "EUR",
        "RUR",
        "CHF",
        "GBP",
        "PLZ",
        "SEK",
        "XAU",
        "CAD",
    )

    print(Fore.GREEN + "[>] Available currencies:")
    print(Fore.GREEN + "[>]", Fore.GREEN + ", ".join(available_currencies))

    currency = safe_input(
        "[>] Insert currency",
        validator=lambda inp: inp.upper() in available_currencies,
        post_processor=str.upper,
    )

    start_date = safe_input(
        "[>] Insert start date (format %d.%m.%Y): ",
        validator=string_per_date,
        post_processor=string_per_date,
    )

    end_date = datetime.now()

    if start_date < end_date:
        print(Fore.GREEN + f"[>] Currency: {currency}")
        last_sale_rate_nb = 0

        for date in date_range(start_date, end_date):
            responce = make_request({"date": date})

            if responce:
                print(Fore.GREEN + f"[>] Date: {date}")

                for rate in responce.get("exchangeRate", list()):
                    if rate.get("currency") == currency:
                        sale_rate_nb = rate["saleRateNB"]

                        if last_sale_rate_nb == 0:
                            difference = "-------"
                        else:
                            difference = round(sale_rate_nb - last_sale_rate_nb, 4)

                        last_sale_rate_nb = sale_rate_nb

                        print(Fore.GREEN + f"[>] NBU: {sale_rate_nb}  \t  {difference}")

            else:
                print(Fore.RED + "[!] Empty responce")

            time.sleep(0.5)

    else:
        print(Fore.RED + "[!] Start date is the larger current date")


if __name__ == "__main__":
    main()
