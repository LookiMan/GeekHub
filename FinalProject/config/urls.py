"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
import os

from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.staticfiles.views import serve
from django.http import Http404
from django.conf import settings


def return_file(request, path, insecure=True, **kwargs):
    if not settings.DEBUG and not insecure:
        raise Http404(f"File Not Found: {path}")

    return serve(request, path, insecure, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("telegram/", include("telegram_bot.urls")),
]


if settings.DEBUG:
    urlpatterns += (
        re_path(r"^static/(?P<path>.*)$", return_file, name="static"),
        re_path(r"^media/(?P<path>.*)$", return_file, name="media"),
        re_path(r"^photos/(?P<path>.*)$", return_file, name="photos"),
    )
