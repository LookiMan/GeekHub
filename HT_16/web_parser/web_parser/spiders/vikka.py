from datetime import datetime

import scrapy

from web_parser import items

"""

Переробити попереднє домашнє завдання: зберігати результати в базу, використовуючи pipelines.

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

    def start_requests(self):
        yield scrapy.Request(f'https://www.vikka.ua/{self.date}/', callback=self.parse_page)

    def parse_page(self, response):
        for href in response.css('a.more-link-style::attr("href")').getall():
            url = response.urljoin(href)

            yield scrapy.Request(url, callback=self.parse_new)

        href = response.css('a.page-numbers.next::attr("href")').get()
        if href:
            yield scrapy.Request(href, callback=self.parse_page)

    def parse_new(self, response):
        item = items.WebparserItem()

        item["url"] = response.request.url
        item["title"] = response.css("h1.post-title::text").get()
        item["text"] = response.css("div.entry-content ::text").getall()
        item["tags"] = [
            "#"+tag for tag in response.css("a.post-tag::text").getall()]
        item["date"] = self.date

        yield item
