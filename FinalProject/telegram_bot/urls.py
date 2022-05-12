from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from telegram_bot import api

app_name = "telegram_bot"

urlpatterns = [
    path("webhook/<str:token>/",
         csrf_exempt(api.telegram_webhook), name="telegram_webhook"),
    path("block_user/<int:user_id>/", api.block_user, name="block_user"),
    path("unblock_user/<int:user_id>/", api.unblock_user, name="unblock_user"),
    path("get_user_photo/<str:file_id>/", api.user_photo, name="user_photo"),
]
