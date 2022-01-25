"""
Використовуючи бібліотеку requests написати скрейпер для отримання статей / записів із АПІ
Документація на АПІ:
https://github.com/HackerNews/API
Скрипт повинен отримувати із командного рядка одну із наступних категорій:
askstories, showstories, newstories, jobstories
Якщо жодної категорії не указано - використовувати newstories.
Якщо категорія не входить в список - вивести попередження про це і завершити роботу.
Результати роботи зберегти в CSV файл. Зберігати всі доступні поля. Зверніть увагу - інстанси різних типів мають різний набір полів.
Код повинен притримуватися стандарту pep8.
Перевірити свій код можна з допомогою ресурсу http://pep8online.com/
Для тих, кому хочеться зробити щось "додаткове" - можете зробити наступне: другим параметром cкрипт може приймати
назву HTML тега і за допомогою регулярного виразу видаляти цей тег разом із усим його вмістом із значення атрибута "text"
(якщо він існує) отриманого запису.
"""

import io
import re
import sys
import csv

import requests


def get_specified_category():
    avalible_categories = (
        "askstories",
        "showstories",
        "newstories",
        "jobstories",
    )

    tag = sys.argv[2] if len(sys.argv) > 2 else None

    if len(sys.argv) == 1:
        selected_category = "newstories"
    elif sys.argv[1] in avalible_categories:
        selected_category = sys.argv[1]
    else:
        print(f"[!] Категорії '{sys.argv[1]}' немає в списку доступних")
        print("[i] Доступні категорії:", ", ".join(avalible_categories))
        exit(1)

    return tag, selected_category


def get_stories_id_by_category_name(category):
    url = f"https://hacker-news.firebaseio.com/v0/{category}.json"
    response = requests.get(url, {"print": "pretty"})

    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_story_by_id(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    response = requests.get(url, {"print": "pretty"})

    if response.status_code == 200:
        return response.json()
    else:
        return {}


def replace_tags(tag, text):
    for string in re.findall(f'<{tag}>.*?<{tag}>', text):
        text = text.replace(string, "")
    return text


class CsvItemExporter(object):
    def __init__(self, file, include_headers_line=True, join_multivalued=',', errors=None, **kwargs):
        self._kwargs = kwargs
        self.encoding = 'utf-8'
        self.include_headers_line = include_headers_line
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline='',
            errors=errors,
        )
        self.csv_writer = csv.writer(self.stream, **self._kwargs)
        self._headers_not_written = True
        self._join_multivalued = join_multivalued
        self.fields_to_export = None
        return

    def start_exporting(self):
        pass

    def finish_exporting(self):
        pass

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item, default_value='',
                                             include_empty=True)
        values = list(self._build_row(x for _, x in fields))
        self.csv_writer.writerow(values)
        return

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        output = []

        if include_empty is None:
            include_empty = self.export_empty_fields

        if include_empty:
            field_iter = self.fields_to_export
        else:
            field_iter = (x for x in self.fields_to_export if x in item)

        for field_name in field_iter:
            if field_name in item:

                value = self.serialize_field(item[field_name])
            else:
                value = default_value

            output.append((field_name, value))
        return output

    def serialize_field(self, value):
        return self._join_if_needed(value)

    def to_unicode(self, text, encoding=None, errors='strict'):
        if isinstance(text, str):
            return text
        if not isinstance(text, (bytes, str)):
            raise TypeError('to_unicode must receive a bytes or str '
                            f'object, got {type(text).__name__}')
        if encoding is None:
            encoding = 'utf-8'
        return text.decode(encoding, errors)

    def _join_if_needed(self, value):
        if isinstance(value, (list, tuple)):
            try:
                return self._join_multivalued.join(value)
            except TypeError:
                pass
        return value

    def _build_row(self, values):
        output = []
        for value in values:
            try:
                output.append(self.to_unicode(value, self.encoding))
            except TypeError:
                output.append(value)
        return output

    def _write_headers_and_set_fields_to_export(self, item):
        if self.include_headers_line:
            row = list(self._build_row(self.fields_to_export))
            self.csv_writer.writerow(row)


class CsvExporter(object):
    def __init__(self, filename, fields_to_export):
        self.file = open(filename, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = fields_to_export
        self.exporter.start_exporting()

    def close(self):
        self.exporter.finish_exporting()
        self.file.close()
        return

    def process_item(self, item):
        self.exporter.export_item(item)
        return


def main():
    tag, selected_category = get_specified_category()

    fields_to_export = (
        "by",
        "descendants",
        "id",
        "score",
        "time",
        "title",
        "kids",
        "type",
        "text",
        "url",
    )

    exporter = CsvExporter("./output.csv", fields_to_export)

    for story_id in get_stories_id_by_category_name(selected_category):
        story = get_story_by_id(story_id)

        if tag and story.get("text"):
            story["text"] = replace_tags(tag, story["text"])

        exporter.process_item(story)

    exporter.close()


if __name__ == "__main__":
    main()
