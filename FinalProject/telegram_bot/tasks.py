import os
import sys

from telebot import TeleBot, types

from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer

from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from config.settings import TELEGRAM_BOT_TOKEN, WEBHOOK_HOST
from config.celery import app

from chat.models import Chat, Message

from telegram_bot.models import User
from telegram_bot import utils


# https://habr.com/ru/post/502380/

if not TELEGRAM_BOT_TOKEN:
    raise BaseException(
        "TELEGRAM_BOT_API_TOKEN not found in OS enviroment paths")


if not WEBHOOK_HOST:
    raise BaseException(
        "WEBHOOK_HOST not found in OS enviroment paths")


WEBHOOK_PATH = f"/{TELEGRAM_BOT_TOKEN}/"
WEBHOOK_URL = WEBHOOK_HOST + "/telegram/telegram_api" + WEBHOOK_PATH


IGNORED_CONTENT_TYPES = [
    "audio",
    "sticker",
    "video",
    "video_note",
    "voice",
    "location",
    "contact"
]


bot = TeleBot(token=TELEGRAM_BOT_TOKEN)


if "--not-set-telegram-webhook" not in sys.argv:
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)

    sys.argv.append("--not-set-telegram-webhook")


def _download_file_from_telegram(file_id):
    metadata = bot.get_file(file_id)
    content = bot.download_file(metadata.file_path)

    utils.save_file(content, file_id)


@async_to_sync
async def notify_staff_about_new_chat(chat):
    await get_channel_layer().group_send(
        "chat", {
            "type": "notify.staff",
            "ucid": chat.ucid,
            "first_name": chat.first_name,
            "last_name": chat.last_name,
            "username": chat.username,
            "user_image": chat.user.image.url,
        }
    )


def send_text_message_to_client(chat, text, reply_to_message_id=None):
    message = bot.send_message(
        chat.id,
        text=mark_safe(text),
        reply_markup=None,
        parse_mode="HTML",
        reply_to_message_id=reply_to_message_id
    )

    process_message(chat, message)


@sync_to_async
def async_send_text_message_to_client(chat, text, reply_to_message_id=None):
    send_text_message_to_client(chat, text, reply_to_message_id)


def send_photo_to_client(chat, file, *, caption=None, reply_to_message_id=None):
    message = bot.send_photo(
        chat.id,
        file,
        caption=mark_safe(caption),
        reply_to_message_id=reply_to_message_id,
    )

    _download_file_from_telegram(message.photo[-1].file_id)
    process_message(chat, message)


def send_document_to_client(chat, file, *, caption=None, reply_to_message_id=None):
    message = bot.send_document(
        chat.id,
        file,
        caption=mark_safe(caption),
        reply_to_message_id=reply_to_message_id,
    )

    _download_file_from_telegram(message.document.file_id)
    process_message(chat, message)


def send_welcome_message(message):
    first_name = message.chat.first_name or ""
    last_name = message.chat.last_name or ""
    username = message.chat.username or ""

    username = message.chat.username or first_name + " " + last_name

    bot.send_message(
        message.chat.id,
        text=f"<i>Привет, {mark_safe(username)}👋\n</i>",
        parse_mode='HTML',
    )


def send_message_to_user_about_blocking(telegram_user):
    try:
        chat_id = telegram_user.chats.get(user=telegram_user).id
    except ObjectDoesNotExist:
        pass
    else:
        bot.send_message(
            chat_id,
            "❌ Вы заблокированы ❌",
            parse_mode="HTML"
        )


def send_message_to_user_about_unblocking(telegram_user):
    try:
        chat_id = telegram_user.chats.get(user=telegram_user).id
    except ObjectDoesNotExist:
        pass
    else:
        bot.send_message(
            chat_id,
            "❌ Вы заблокированы ❌",
            parse_mode="HTML"
        )


def get_or_create_telegram_user(message):
    return User.objects.get_or_create(
        id=message.from_user.id,
        is_bot=message.from_user.is_bot,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
    )


def get_or_create_telegram_chat(telegram_user, message):
    return Chat.objects.get_or_create(
        id=message.chat.id,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name,
        username=message.chat.username,
        type=message.chat.type,
        user=telegram_user,
    )


def get_telegram_user(message):
    telegram_user, is_new = get_or_create_telegram_user(message)

    if is_new:
        filename = download_user_photo(message.from_user.id)

        if filename:
            telegram_user.image.name = filename
            telegram_user.save()

        send_welcome_message(message)

    return telegram_user


def get_telegram_chat(user, message):
    chat, is_new = get_or_create_telegram_chat(user, message)

    if is_new:
        notify_staff_about_new_chat(chat)

    return chat


@bot.message_handler(content_types=IGNORED_CONTENT_TYPES)
def process_ignored_content_types(message):
    text = "⚠️ На данный момент \nбот поддерживает "\
        "следущие типы сообщений:"\
        "\n\n📝 Текст"\
        "\n\n🖼 Фото"\
        "\n\n📁 Файлы"\

    bot.send_message(
        message.chat.id,
        text=text
    )


def process_message(chat, message):
    document = message.document.file_id if message.document else None
    file_name = message.document.file_name if message.document else None
    photo = message.photo[-1].file_id if message.photo else None
    caption = message.caption if message.caption else None

    staff = chat.staff if message.from_user.is_bot else None
    user = chat.user if not message.from_user.is_bot else None

    if message.reply_to_message:
        try:
            reply_to_message = Message.objects.get(
                id=message.reply_to_message.message_id,
                chat=chat,
            )
        except ObjectDoesNotExist:
            reply_to_message = None
    else:
        reply_to_message = None

    return Message.objects.create(
        id=message.message_id,
        chat=chat,
        user=user,
        staff=staff,
        reply_to_message=reply_to_message,
        text=message.text,
        photo=photo,
        document=document,
        file_name=file_name,
        caption=caption,
    )


@bot.message_handler(content_types=["text"])
def process_received_text_message(message):
    user = get_telegram_user(message)
    chat = get_telegram_chat(user, message)

    if user.is_blocked:
        send_message_to_user_about_blocking(user)
    else:
        process_message(chat, message)


@bot.message_handler(commands=["start"])
def process_received_start_commant(message):
    process_received_text_message(message)


@bot.message_handler(content_types=["photo"])
def process_received_photo_message(message):
    user = get_telegram_user(message)
    chat = get_telegram_chat(user, message)

    if user.is_blocked:
        send_message_to_user_about_blocking(user)
    else:
        _download_file_from_telegram(message.photo[-1].file_id)
        process_message(chat, message)


@bot.message_handler(content_types=["document"])
def process_received_document_message(message):
    user = get_telegram_user(message)
    chat = get_telegram_chat(user, message)

    if user.is_blocked:
        send_message_to_user_about_blocking(user)
    else:
        _download_file_from_telegram(message.document.file_id)
        process_message(chat, message)


@app.task()
def process_telegram_event(update):
    update = types.Update.de_json(update)
    bot.process_new_updates([update])


def download_user_photo(user_id):
    response = bot.get_user_profile_photos(user_id)

    if response.total_count > 0:
        file_id = response.photos[0][0].file_id

        metadata = bot.get_file(file_id)
        _, extention = os.path.splitext(metadata.file_path)

        content = bot.download_file(metadata.file_path)

        return utils.save_user_image(content, file_id + extention)

    return None


def debug_telegram_bot():
    bot.remove_webhook()
    bot.polling()
