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

from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from django.conf import settings

from chat.tasks import google_drive_serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("telegram/", include("telegram_bot.urls")),
    path(r"media/<str:file_id>", google_drive_serve, name="media"),
]


if settings.DEBUG:
    urlpatterns += (
        path(r"static/<path:path>", never_cache(serve), name="static"),  
    )
