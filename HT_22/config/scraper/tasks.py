import re

import requests

from scraper import models
from scraper import utils
from config import celery


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


class DjangoItemExporter(object):
    def __init__(self, category):
        self.category = category

    def start_exporting(self):
        pass

    def finish_exporting(self):
        pass

    def export_item(self, item):
        if self.category == "askstories":
            models.Ask.objects.get_or_create(
                by=item.get("by", 0),
                descendants=item.get("descendants", ""),
                ask_id=item.get("id", 0),
                score=item.get("score", 0),
                text=item.get("text", ""),
                time=utils.ctime(item.get("time", 0)),
                title=item.get("title", ""),
            )

        elif self.category == "jobstories":
            models.Job.objects.get_or_create(
                by=item.get("by", 0),
                job_id=item.get("id", 0),
                score=item.get("score", 0),
                text=item.get("text", ""),
                time=utils.ctime(item.get("time", 0)),
                title=item.get("title", ""),
                url=item.get("url", ""),
            )

        elif self.category in ("newstories", "showstories"):
            models.Story.objects.get_or_create(
                by=item.get("by", 0),
                descendants=item.get("descendants", ""),
                story_id=item.get("id", 0),
                score=item.get("score", 0),
                time=utils.ctime(item.get("time", 0)),
                title=item.get("title", ""),
                url=item.get("url", ""),
            )

        return


class DjangoExporter(object):
    def __init__(self, category):
        self.exporter = DjangoItemExporter(category)
        return

    def close(self):
        self.exporter.finish_exporting()
        return

    def process_item(self, item):
        self.exporter.export_item(item)
        return


@ celery.celery_app.task(name="scraper.tasks.start_scraping", queue="scraper")
def start_scraping(category, tag=None):
    exporter = DjangoExporter(category)

    if category == "askstories":
        exclude = [obj.ask_id for obj in models.Ask.objects.all()]
    elif category == "jobstories":
        exclude = [obj.job_id for obj in models.Job.objects.all()]
    elif category in ("newstories", "showstories"):
        exclude = [obj.story_id for obj in models.Story.objects.all()]
    else:
        exclude = []

    for story_id in get_stories_id_by_category_name(category):
        if story_id not in exclude:
            story = get_story_by_id(story_id)
            if story:
                if tag and story.get("text"):
                    story["text"] = replace_tags(tag, story["text"])

                exporter.process_item(story)

    exporter.close()
    return
