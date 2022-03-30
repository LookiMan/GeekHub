from django.urls import path

from chat import consumers
from telegram_bot import api

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
