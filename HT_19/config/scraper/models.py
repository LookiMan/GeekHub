from django.db import models


class Ask(models.Model):
    by = models.CharField(max_length=128)
    descendants = models.IntegerField()
    ask_id = models.IntegerField()
    score = models.IntegerField()
    text = models.TextField()
    time = models.DateTimeField()
    title = models.TextField()

    def __str__(self):
        return f"Ask: id {self.ask_id}"


class Job(models.Model):
    by = models.CharField(max_length=128)
    job_id = models.IntegerField()
    score = models.IntegerField()
    text = models.TextField()
    time = models.DateTimeField()
    title = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"Job: id {self.job_id}"


class Story(models.Model):
    by = models.CharField(max_length=128)
    descendants = models.IntegerField()
    story_id = models.IntegerField()
    score = models.IntegerField()
    time = models.DateTimeField()
    title = models.TextField()
    url = models.URLField()

    def __str__(self):
        return f"Story: id {self.story_id}"
