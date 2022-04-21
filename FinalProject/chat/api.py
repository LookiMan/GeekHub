from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from chat.forms import UploadFileForm
from chat.models import Chat, Message
from chat.serializers import ChatSerializer, MessageSerializer
from chat.utils import logger

from telegram_bot.tasks import send_photo_to_client, send_document_to_client


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def get_chat(request, ucid):
    try:
        chat = Chat.objects.get(ucid=ucid)
    except Chat.DoesNotExist:
        return Response(f'Chat not found', status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(f'{exc}. Payload: ucid: {ucid}')
        return Response('Unclassified error', status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:

        if not chat.staff:
            chat.staff = request.user
            chat.save()

        serializer = ChatSerializer(chat)
        return Response(serializer.data)


@api_view(('GET',))
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
        return Response('Unclassified error', status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = ChatSerializer(chat)
        return Response(serializer.data)


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def get_chats(request):
    try:
        chats = Chat.objects.all().exclude(is_note=True)
    except Chat.DoesNotExist:
        return Response(f'Chats not found', status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(exc)
        return Response('Unclassified error', status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
def get_messages(request, ucid, offset):
    try:
        messages = Message.objects.filter(chat=ucid).exclude(id__lte=offset)
    except Message.DoesNotExist:
        return Response(f'Messages not found', status=HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.exception(f'{exc}. Payload: ucid: {ucid}; offset: {offset};')
        return Response('Unclassified error', status=HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


@api_view(('GET',))
@permission_classes((IsAuthenticated,))
@renderer_classes((TemplateHTMLRenderer,))
def get_emojis(request):
    return Response(template_name="./chat/emoji.html")


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
        ucid = form.cleaned_data.get("ucid")

        try:
            chat = Chat.objects.get(ucid=ucid)
        except Chat.DoesNotExist:
            Response({
                "code": 400, "errors":  {
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

            return Response({"code": 200}, status=HTTP_201_CREATED)

    return Response({"code": 400, "errors": form.errors}, status=HTTP_400_BAD_REQUEST)