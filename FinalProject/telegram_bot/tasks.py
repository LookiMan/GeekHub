from telebot import types

from config.celery import app
from telegram_bot.bot import bot


@app.task()
def process_telegram_event(update):
    update = types.Update.de_json(update)
    bot.process_new_updates([update])
