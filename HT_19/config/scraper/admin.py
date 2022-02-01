from django.contrib import admin

from . import models


@admin.register(models.Ask)
class AskAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    pass
