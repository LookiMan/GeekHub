from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from chat.forms import UploadFileForm
from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer
from chat.tasks import upload_to_google_drive
from chat.utils import logger, ctime

from telegram_bot.bot import send_photo_to_client, send_document_to_client, delete_bot_message


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def get_chat(request, ucid):
    try:
        chat = Chat.objects.get(ucid=ucid)
    except Chat.DoesNotExist:
        return Response(f"Chat not found", status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(f"{exc}. Payload: ucid: {ucid}")
        return Response("Unclassified error", status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:

        if not chat.staff:
            chat.staff = request.user
            chat.save()

        serializer = ChatSerializer(chat)
        return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def get_note(request):
    try:
        chat, _ = Chat.objects.get_or_create(
            id=request.user.pk,
            first_name="Мои заметки",
            last_name=None,
            username=None,
            is_note=True,
            staff=request.user,
        )
    except Exception as exc:
        logger.exception(exc)
        return Response("Unclassified error", status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = ChatSerializer(chat)
        return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def get_chats(request):
    try:
        chats = Chat.objects.all().filter(is_archived=False).exclude(is_note=True)
    except Chat.DoesNotExist:
        return Response(f"Chats not found", status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(exc)
        return Response("Unclassified error", status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated, IsSuperuser))
def get_archived_chats(request):
    try:
        chats = Chat.objects.all().filter(is_archived=True).exclude(is_note=True)
    except Chat.DoesNotExist:
        return Response(f"Chats not found", status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(exc)
        return Response("Unclassified error", status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def get_messages(request, ucid):
    try:
        messages = Message.objects.filter(chat=ucid)
    except Message.DoesNotExist:
        return Response({
            "success": False,
            "description": f"Сообщение с ucid '{ucid}' не найдено",
            "ucid": ucid,
        },
            status=HTTP_400_BAD_REQUEST
        )
    except Exception as exc:
        logger.exception(f"{exc}. Payload: ucid: {ucid};")
        return Response({
            "success": False,
            "description": "Непредвиденная ошибка сервера",
        },
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    else:
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
@renderer_classes((TemplateHTMLRenderer,))
def get_emojis(request):
    return Response(template_name="./chat/emoji.html")


@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
        ucid = form.cleaned_data.get("ucid")

        try:
            chat = Chat.objects.get(ucid=ucid)
        except Chat.DoesNotExist:
            Response({
                "code": HTTP_400_BAD_REQUEST, "errors":  {
                    "chat": f"Чат с ucid '{ucid}' не найден"
                }
            },
                status=HTTP_400_BAD_REQUEST
            )
        else:
            photo = form.cleaned_data.get("photo")
            document = form.cleaned_data.get("document")
            caption = form.cleaned_data.get("caption")
            reply_to_message_id = form.cleaned_data.get("reply_to_message_id")

            if chat.is_note:
                message_id = form.cleaned_data.get("message_id")
                file_name = form.cleaned_data.get("file_name")
                date = form.cleaned_data.get("date")

                if reply_to_message_id:
                    try:
                        reply_to_message = Message.objects.get(
                            id=reply_to_message_id,
                            chat=chat,
                        )
                    except Message.DoesNotExist:
                        reply_to_message = None
                else:
                    reply_to_message = None

                Message.objects.create(
                    id=message_id,
                    chat=chat,
                    user=None,
                    staff=chat.staff,
                    reply_to_message=reply_to_message,
                    text=None,
                    photo=upload_to_google_drive(
                        file_name, photo.read()) if photo else None,
                    document=upload_to_google_drive(
                        file_name, document.read()) if document else None,
                    file_name=file_name,
                    caption=caption,
                    date=ctime(date),
                )

            else:
                if photo:
                    send_photo_to_client(
                        chat,
                        photo,
                        caption=caption,
                        reply_to_message_id=reply_to_message_id
                    )

                elif document:
                    send_document_to_client(
                        chat,
                        document,
                        caption=caption,
                        reply_to_message_id=reply_to_message_id
                    )

            return Response({"code": HTTP_201_CREATED}, status=HTTP_201_CREATED)

    return Response({"code": HTTP_400_BAD_REQUEST, "errors": form.errors}, status=HTTP_400_BAD_REQUEST)


def change_chat_archive_state(request, ucid, *, is_archived):
    try:
        chat = Chat.objects.get(ucid=ucid)
        chat.is_archived = is_archived
        chat.save(update_fields=["is_archived"])
    except Chat.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Некорректный запрос. Чат с ucid '{ucid}' не найден",
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
        state = "заархивирован" if chat.is_archived else "разархивирован"

        return Response({
            "success": True,
            "description": f"Чат с ucid '{ucid}' {state}",
            "ucid": ucid,
        })


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def archive_chat(request, ucid):
    return change_chat_archive_state(request, ucid, is_archived=True)


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def unarchive_chat(request, ucid):
    return change_chat_archive_state(request, ucid, is_archived=False)


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def edit_message(request, message_id, text):
    update_fields = []

    try:
        message = Message.objects.get(id=message_id)

        if message.text:
            message.text = text
            update_fields.append("text")
        elif message.caption:
            message.text = caption
            update_fields.append("text")

        message.save(update_fields=update_fields)
    except Message.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Некорректный запрос. Сообщение с id '{message_id}' не найдено в базе данных",
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
        try:
            delete_bot_message(message.chat.id, message_id)
        except Exception as exc:
            logger.exception(exc)
            return Response({
                "success": False,
                "description": f"Сообщение с id '{message_id}' помечено как удаленное, но не удалено в telegram-чате",
                "id": message_id,
            })
        else:
            return Response({
                "success": True,
                "description": f"Сообщение с id '{message_id}' успешно помечено как удаленное",
                "id": message_id,
            })


@api_view(("DELETE",))
@permission_classes((IsAuthenticated,))
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_deleted = True
        message.save(update_fields=["is_deleted"])
    except Message.DoesNotExist as exc:
        logger.exception(exc)
        return Response({
            "success": False,
            "description": f"Некорректный запрос. Сообщение с id '{message_id}' не найдено в базе данных",
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
        try:
            if not message.chat.is_note:
                delete_bot_message(message.chat.id, message_id)
        except Exception as exc:
            logger.exception(exc)
            return Response({
                "success": False,
                "description": f"Сообщение с id '{message_id}' помечено как удаленное, но не удалено в telegram-чате",
                "id": message_id,
            })
        else:
            return Response({
                "success": True,
                "description": f"Сообщение с id '{message_id}' успешно помечено как удаленное",
                "id": message_id,
            })
