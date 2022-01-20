# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from scrapy.exporters import BaseItemExporter


class SqliteItemExporter(BaseItemExporter):
    def __init__(self, db_file, *, dont_fail=False, **kwargs):
        super().__init__(dont_fail=dont_fail, **kwargs)
        self.db_file = db_file

    def create_connection(self):
        self.conn = sqlite3.connect(self.db_file)
        self.curr = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def create_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS output (
                        title TEXT, text TEXT, tags TEXT, link TEXT, date TEXT
                        )""")

    def start_exporting(self):
        self.create_connection()
        self.create_table()

    def finish_exporting(self):
        self.close_connection()

    def export_item(self, item):
        item = dict(self._get_serialized_fields(item))

        self.curr.execute("""INSERT INTO output VALUES (?, ?, ?, ?, ?)""", (
            item['title'], item['text'], item["tags"], item["url"], item["date"]
        ))
        self.conn.commit()


class SqlLiteExportPipeline(object):
    """ 
    Клас зберігає дані в базу даних sqlite. 
    """

    def __init__(self):
        self.db_file = "./db.sqlite3"

    def open_spider(self, spider):
        self.exporter = SqliteItemExporter(self.db_file)
        self.exporter.fields_to_export = [
            "title", "text", "tags", "url", "date"]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
