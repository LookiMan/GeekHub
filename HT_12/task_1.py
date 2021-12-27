"""
1. http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної інформації про записи:
   цитата, автор, інфа про автора... Отриману інформацію зберегти в CSV файл та в базу. Результати зберегти в репозиторії.
   Пагінацію по сторінкам робити динамічною (знаходите лінку на наступну сторінку і берете з неї URL). Хто захардкодить
   пагінацію зміною номеру сторінки в УРЛі - буде наказаний ;)
"""

import utils


def main():
    root_url = "http://quotes.toscrape.com/"
    output_csv_file = "./output/output.csv"
    output_db_file = "./output/output.db"

    url = root_url

    while True:
        html = utils.get_html_code_of_page(url)
        soup = utils.get_soup_from_html(html)

        for quote in utils.select_all_quote(soup):
            quote_data = utils.select_quote_data(quote)

            author_profile = quote_data.get("author_profile")

            if author_profile:
                author_data = utils.select_about_author_data(root_url + author_profile)
                quote_data.update(**author_data)

            utils.save_quotes_to_csv(output_csv_file, quote_data)
            utils.save_quotes_to_db(output_db_file, quote_data)

        url_next_page = utils.select_next_page_link(soup)

        if not url_next_page:
            break

        url = root_url + url_next_page


if __name__ == "__main__":
    main()
