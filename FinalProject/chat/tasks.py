from django.http import StreamingHttpResponse

from config.celery import app

from chat.utils import generator
from telegram_bot.bot import g_drive


@app.task()
def google_drive_serve(request, file_id, *args, **kwargs):
    content = g_drive.get_file(file_id)

    return StreamingHttpResponse(generator(content))


@app.task()
def upload_to_google_drive(filename, content):
    return g_drive.put_file(filename, content)
