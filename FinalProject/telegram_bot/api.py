import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from django.conf import settings
from chat.utils import logger

from telegram_bot.models import User
from telegram_bot.tasks import process_telegram_event
from telegram_bot.tasks import send_message_to_user_about_blocking
from telegram_bot.tasks import send_message_to_user_about_unblocking


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


@api_view(['GET'])
def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = True
        user.save(update_fields=["is_blocked"])
        send_message_to_user_about_blocking(user_id)
    except User.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Bad request. User with id '{user_id}' not found",
        },
            status=HTTP_400_BAD_REQUEST,
        )
    except Exception as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": "Unclassified error",
        },
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response({
            "success": True,
            "description": f"User with id '{user_id}' has been blocked"
        })


@api_view(['GET'])
def unblock_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = False
        user.save(update_fields=["is_blocked"])
        send_message_to_user_about_unblocking(user_id)
    except User.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Bad request. User with id '{user_id}' not found",
        },
            status=HTTP_400_BAD_REQUEST,
        )
    except Exception as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": "Unclassified error",
        },
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response({
            "success": True,
            "description": f"User with id '{user_id}' has been unblocked"
        })
