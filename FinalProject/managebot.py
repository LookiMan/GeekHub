import os
import sys

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

sys.argv.append("--not-set-telegram-webhook")
django.setup()

from telegram_bot.bot import debug_telegram_bot


if __name__ == '__main__':
    debug_telegram_bot()
