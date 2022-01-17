# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from scrapy.exporters import CsvItemExporter


class CsvExportPipeline(object):
    """ 
    Класс зберігає дані в вихідний файл. 
    Ім'я вихідного файлу задається атрибуту output_file класу VikkaSpider
    """

    def open_spider(self, spider):
        self.file = open(spider.output_file, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.fields_to_export = ['title', 'text', 'tags', 'url']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
