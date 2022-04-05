from telegram_bot import tasks
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

sys.argv.append("--not-set-telegram-webhook")
django.setup()


if __name__ == '__main__':
    tasks.debug_telegram_bot()
