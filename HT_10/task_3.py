"""
3. Конвертер валют. Прийматиме від користувача назву двох валют і суму (для першої).
   Робить запрос до API архіву курсу валют Приватбанку (на поточну дату) і виконує
   конвертацію введеної суми з однієї валюти в іншу.
"""

from colorama import init, Fore

from task_1 import safe_input
import utils


init(autoreset=True)


def convert_other_currency_to_uah(
    currency: str, amount_to_exchange: int, exchange_courses: str
) -> float:
    for cours in exchange_courses:
        if cours["ccy"] == currency:
            return amount_to_exchange * float(cours["sale"])


def convert_uah_to_other_currency(
    currency: str, amount_to_exchange: int, exchange_courses: str
) -> float:
    for cours in exchange_courses:
        if cours["ccy"] == currency:
            return amount_to_exchange / float(cours["sale"])


def convert_btc_to_usd(amount_to_exchange: int, exchange_courses: str) -> float:
    for cours in exchange_courses:
        if cours["ccy"] == "BTC":
            return amount_to_exchange * float(cours["sale"])


def convert_usd_to_btc(amount_to_exchange: int, exchange_courses: str) -> float:
    for cours in exchange_courses:
        if cours["ccy"] == "BTC":
            return amount_to_exchange / float(cours["sale"])


def exchanger() -> float:
    available_currencies = (
        "USD",
        "EUR",
        "RUR",
        "BTC",
        "UAH",
    )

    print(Fore.GREEN + "[>] Доступні валюти для обміну:")
    print(Fore.GREEN + "[>]", Fore.GREEN + ", ".join(available_currencies))

    first_currency = safe_input(
        "[>] вкажіть першу валюту",
        validator=lambda inp: inp.upper() in available_currencies,
        post_processor=str.upper,
    )

    second_currency = safe_input(
        "[>] вкажіть другу валюту",
        validator=lambda inp: inp.upper() in available_currencies,
        post_processor=str.upper,
    )

    amount_to_exchange = safe_input(
        "[>] вкажіть суму для обміну", validator=int, post_processor=int
    )

    exchange_courses = utils.make_exchange_currency_request({"coursid": 5})

    if exchange_courses:

        if "BTC" in (first_currency, second_currency):
            if first_currency == "BTC":
                usd = convert_btc_to_usd(amount_to_exchange, exchange_courses)

                if second_currency == "USD":
                    return usd

                uah = convert_other_currency_to_uah("USD", usd, exchange_courses)
            
                return convert_uah_to_other_currency(
                    second_currency, uah, exchange_courses
                )

            else:
                if first_currency == "UAH":
                    uah = amount_to_exchange
                else:
                    uah = convert_other_currency_to_uah(first_currency, amount_to_exchange, exchange_courses)       
                
                usd = convert_uah_to_other_currency("USD", uah, exchange_courses)
            
                if second_currency == "USD":
                    return usd

                return convert_usd_to_btc(usd, exchange_courses)

        else:
            if first_currency == "UAH":
                return convert_uah_to_other_currency(
                    second_currency, amount_to_exchange, exchange_courses
                )

            else:
                uah = convert_other_currency_to_uah(
                    first_currency, amount_to_exchange, exchange_courses
                )

                if second_currency == "UAH":
                    return uah

                else:
                    return convert_uah_to_other_currency(
                        second_currency, uah, exchange_courses
                    )

    else:
        print(Fore.RED + "[!] Неможливо отримати курси обміну валют")


def main() -> None:
    result = exchanger()

    print(Fore.GREEN + "[>] ==================")
    print(Fore.GREEN + f"[>] {round(result, 3)}")


if __name__ == "__main__":
    main()
