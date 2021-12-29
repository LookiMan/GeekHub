import csv
import os
import sqlite3

import requests

from bs4 import BeautifulSoup, element


_about_authors_data_cahce = {}


def save_quotes_to_csv(filename: str, data: dict) -> list:
    is_file_existed = os.path.exists(filename)

    fieldnames = data.keys()
    with open(filename, mode="a", encoding="utf8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, delimiter="|", fieldnames=fieldnames)

        if not is_file_existed:
            writer.writeheader()

        writer.writerow(data)


def save_quotes_to_db(filename: str, quote_data: dict) -> None:
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    query = """INSERT INTO quotes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(query, tuple(quote_data.values()))
    connection.commit()
    connection.close()


def get_html_code_of_page(url: str, params: dict = None) -> str:
    responce = requests.get(url, params=params)

    return responce.text


def get_soup_from_html(html: str, parser: str = "lxml") -> BeautifulSoup:
    return BeautifulSoup(html, parser)


def select_all_quote(soup: BeautifulSoup) -> BeautifulSoup:
    return soup.select("div.quote")


def select_quote_text(soup: BeautifulSoup) -> str:
    return soup.select_one('span[itemprop="text"]').text


def select_quote_author(soup: BeautifulSoup) -> str:
    return soup.select_one('small[itemprop="author"]').text


def select_profile_author(soup: BeautifulSoup) -> str:
    element = soup.select_one('small[itemprop="author"] + a[href]')

    return element.get("href") if element else None


def select_quote_tags(soup: BeautifulSoup) -> str:
    return ", ".join([tag.text for tag in soup.select("div.tags > a.tag")])


def select_author_title(soup: BeautifulSoup) -> str:
    return soup.select_one("h3.author-title").text


def select_author_born_date(soup: BeautifulSoup) -> str:
    return soup.select_one("span.author-born-date").text


def select_author_born_location(soup: BeautifulSoup) -> str:
    return soup.select_one("span.author-born-location").text


def select_author_description(soup: BeautifulSoup) -> str:
    return soup.select_one("div.author-description").text


def select_next_page_link(soup: BeautifulSoup) -> str:
    element = soup.select_one("li.next > a[href]")

    return element.get("href") if element else None


def select_quote_data(quote: BeautifulSoup) -> dict:
    return {
        "quote_text": select_quote_text(quote),
        "quote_author": select_quote_author(quote),
        "author_profile": select_profile_author(quote),
        "quote_tags": select_quote_tags(quote),
    }


def select_about_author_data(url: str) -> dict:
    cached_author_data = _about_authors_data_cahce.get(url)

    if cached_author_data:
        return cached_author_data
    else:
        html = get_html_code_of_page(url)
        soup = get_soup_from_html(html)

        author_data = {
            "author_name": select_author_title(soup),
            "born_date": select_author_born_date(soup),
            "born_location": select_author_born_location(soup),
            "description": select_author_description(soup),
        }

        _about_authors_data_cahce[url] = author_data

        return author_data
