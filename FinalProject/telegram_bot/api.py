import json

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from django.conf import settings
from chat.utils import logger
from google_drive_API.api import google_drive_serve

from telegram_bot.models import User
from telegram_bot.bot import send_message, process_telegram_event, BOT_PHRASES


@api_view(("POST",))
def telegram_webhook(request, token):
    update = json.loads(request.body)

    if token != settings.TELEGRAM_BOT_TOKEN:
        return Response(
            "Bad request. Invalid telegram bot token",
            status=HTTP_400_BAD_REQUEST,
        )
    try:
        process_telegram_event(update)

    except Exception as exc:
        logger.exception(exc)
        return Response(
            'Unclassified error',
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        return Response({"code": HTTP_200_OK})


@api_view(("GET",))
def user_photo(request, file_id):
    return google_drive_serve(request, file_id)


def change_user_blocked_state(request, user_id, *, is_blocked):
    try:
        user = User.objects.get(id=user_id)
        user.is_blocked = is_blocked
        user.save(update_fields=["is_blocked"])
    except User.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Некорректный запрос. Пользователь с id '{user_id}' не найден",
        },
            status=HTTP_400_BAD_REQUEST,
        )
    except Exception as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": "Непредвиденная ошибка сервера",
        },
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        state = "заблокирован" if is_blocked else "разблокирован"
        text = BOT_PHRASES["user_blocked"] if user.is_blocked else BOT_PHRASES["user_unblocked"]

        try:
            send_message(user.id, text)
        except:
            return Response({
                "success": False,
                "description": f"Пользователь с id '{user.id}' {state}. Но не получил сообщение в телеграмме",
                "user_id": user.id,
                "is_blocked": user.is_blocked,
            })
        else:
            return Response({
                "success": True,
                "description": f"Пользователь с id '{user.id}' {state}",
                "user_id": user.id,
                "is_blocked": user.is_blocked,
            })


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def block_user(request, user_id):
    return change_user_blocked_state(request, user_id, is_blocked=True)


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def unblock_user(request, user_id):
    return change_user_blocked_state(request, user_id, is_blocked=False)
