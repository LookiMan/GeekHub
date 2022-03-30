from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from telegram_bot import api


app_name = "telegram_bot"

urlpatterns = [
    path("telegram_api/<str:token>/", csrf_exempt(api.telegram_webhook), name="telegram_bot_api"),
]
