import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from django.conf import settings
from chat.utils import logger

from telegram_bot.tasks import process_telegram_event


@api_view(['POST'])
def telegram_webhook(request, token):
    update = json.loads(request.body)

    if token != settings.TELEGRAM_BOT_TOKEN:
        return Response(
            'Bad request. Invalid telegram bot token',
            status=HTTP_400_BAD_REQUEST,
        )

    try:
        if settings.DEBUG:
            process_telegram_event(update)
        else:
            process_telegram_event.delay(update)

    except Exception as exc:
        logger.exception(exc)
        return Response(
            'Unclassified error',
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response({"code": 200})
