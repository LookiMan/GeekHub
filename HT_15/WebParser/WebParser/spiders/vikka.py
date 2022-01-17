from datetime import datetime

import scrapy

from WebParser import items

"""
Легенда:
    - Клієнт для свого проєкта замовив у вас бота, який буде створювати файл з новинами про події у місті за певний день. Клієнт має певні побажання щодо формату файлу, даних у ньому та технологіях, які будуть використовуватися (клієнт планує сам підтримувати свій проєкт, але він знає лише Python та трохи розбирається у Scrapy і BeautifulSoup)
Завдання:
    Напишіть скрейпер для сайту "vikka.ua", який буде приймати від користувача дату, збирати і зберігати інформацію про новини за вказаний день.
Особливості реалізації:
    - використовувати лише Scrapy, BeautifulSoup (опціонально), lxml (опціонально) та вбудовані модулі Python
    - дані повинні зберігатися у csv файл з датою в якості назви у форматі "рік_місяць_число.csv" (напр. 2022_01_13.csv)
    - дані, які потрібно зберігати (саме в такому порядку вони мають бути у файлі):
        1. Заголовок новини
        2. Текст новини у форматі рядка без HTML тегів та у вигляді суцільного тексту (Добре: "Hello world" Погано: "<p>Hello</p><p>world</p>")
        3. Теги у форматі рядка, де всі теги записані з решіткою через кому (#назва_тегу, #назва_тегу, ...)
        4. URL новини
    - збереження даних у файл може відбуватися за бажанням або в самому спайдері, або через Pipelines (буде плюсом в карму)
    - код повинен бути написаний з дотриманням вимог PEP8 (іменування змінних, функцій, класів, порядок імпортів, відступи, коментарі, документація і т.д.)
    - клієнт не повинен здогадуватися, що у вас в голові - додайте якісь підказки там, де це необхідно
    - клієнт може випадково ввести некорректні дані, пам'ятайте про це
    - якщо клієнту доведеться відправляти вам бота на доопрацювання багато разів, або не всі його вимоги будуть виконані - він знайде іншого виконавця, а з вами договір буде розірваний. У нього в команді немає тестувальників, тому перед відправкою завдання - впевніться, що все працює і відповідає ТЗ.
    - не забудьте про requirements.txt
    - клієнт буде запускати бота через термінал командою "scrapy crawl назва_скрейпера"
Корисні посилання:
    - https://www.vikka.ua/
    - https://docs.scrapy.org/en/latest/
    - https://docs.scrapy.org/en/latest/topics/item-pipeline.html


scrapy crawl vikka


"""

# Маска формату дати. Використовується для перевірки коректності введеної дати користувачем
DATE_MASK = "%Y/%m/%d"


def safe_input(prompt, *, validator):
    """
    Безпечне отримання вводу від корисувача 
    """
    while True:
        raw_input = input(f"{prompt}: ").strip()

        try:
            if not validator(raw_input):
                raise Exception()
        except:
            print("[!] введіть корректне значення")
        else:
            return raw_input


def is_valid_date(string):
    """
    Перевірка отриманої строки 
    """
    date = datetime.strptime(string, DATE_MASK)

    if date > datetime.now():
        return False

    return True


class VikkaSpider(scrapy.Spider):
    """
    Скрейпер для сайту "vikka.ua"
    """

    name = 'vikka'
    allowed_domains = ['www.vikka.ua']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.date = safe_input(
            f"[>] Введіть дату для отримання новин (формат {DATE_MASK})",
            validator=is_valid_date,
        )

        filename = self.date.replace("/", "_")

        self.output_file = f"./{filename}.csv"

    def start_requests(self):
        yield scrapy.Request(f'https://www.vikka.ua/{self.date}/', callback=self.parse_page)

    def parse_page(self, response):
        for href in response.css('a.more-link-style::attr("href")').extract():
            url = response.urljoin(href)

            yield scrapy.Request(url, callback=self.parse_new)

    def parse_new(self, response):
        item = items.WebparserItem()

        item["url"] = response.request.url
        item["title"] = response.css("h1.post-title::text").get()
        item["text"] = response.css("div.entry-content p::text").getall()
        item["tags"] = [
            "#"+tag for tag in response.css("a.post-tag::text").getall()]

        yield item
