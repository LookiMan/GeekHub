# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field


def serialize_list(value: list) -> str:
    return ', '.join(value)


def serialize_text(value: list) -> str:
    return ' '.join(value)


class WebparserItem(Item):
    url = Field()
    title = Field()
    text = Field(serializer=serialize_text)
    tags = Field(serializer=serialize_list)
