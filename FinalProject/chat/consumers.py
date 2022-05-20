from email import message
import time

from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer

from chat.models import Chat, Message
from chat.serializers import MessageSerializer, ChatSerializer
from telegram_bot.bot import async_send_text_message_to_client
from telegram_bot.bot import async_edit_bot_message_text, async_edit_bot_message_caption


class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "ucid"

    @action()
    async def join_to_chats(self, **kwargs):
        await self.add_group("chat")

    @action()
    async def edit_text_message(self, text, **kwargs):
        ucid = kwargs.get("ucid")
        message_id = kwargs.get("message_id")

        try:
            chat = await self.get_chat(ucid)
            message = await self.get_message(ucid, message_id)

            message.is_edited = True
            message.edited_text = text

            await self.save_message(message)

        except Exception as exc:
            await self.send_json({
                "action": "error",
                "data": f"Message with id '{message_id}' not found. {exc}",
            })
        else:
            if not chat.is_note:
                if message.text:
                    await async_edit_bot_message_text(chat.id, message_id, text)
                elif message.caption:
                    await async_edit_bot_message_caption(chat.id, message_id, text)

    @action()
    async def send_text_message(self, text, **kwargs):
        ucid = kwargs.get("ucid")
        reply_to_message_id = kwargs.get("reply_to_message_id")

        try:
            chat = await self.get_chat(ucid=ucid)
        except:
            await self.send_json({
                "action": "error",
                "data": f"Чат с ucid '{ucid}' не найден",
            })
        else:
            if chat.is_note:
                await self.create_text_note(chat, text, reply_to_message_id)
            else:
                await async_send_text_message_to_client(chat, text, reply_to_message_id=reply_to_message_id)

    @action()
    async def subscribe_to_messages_in_chat(self, ucid, **kwargs):
        await self.message_activity.subscribe(chat=ucid)

    @action()
    async def unsubscribe_to_messages_in_chat(self, ucid, **kwargs):
        await self.message_activity.unsubscribe(chat=ucid)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'chat__{instance.chat_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, chat=None, **kwargs):
        if chat is not None:
            yield f'chat__{chat}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, umid=instance.umid)

    @ database_sync_to_async
    def get_chat(self, ucid):
        return Chat.objects.get(ucid=ucid)

    @ database_sync_to_async
    def get_message(self, ucid, message_id):
        return Message.objects.filter(id=message_id, chat__ucid=ucid)[0]

    @ database_sync_to_async
    def save_message(self, message):
        message.save(update_fields=["is_edited", "edited_text"])

    @ database_sync_to_async
    def create_text_note(self, chat, text, reply_to_message_id):
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
            id=int(time.time()*10),
            chat=chat,
            user=None,
            staff=chat.staff,
            reply_to_message=reply_to_message,
            text=text,
            photo=None,
            document=None,
            file_name=None,
            caption=None,
        )

    async def notify_staff(self, event):
        data = {
            "action": "createNewChat",
            "data": event,
        }
        await self.send_json(data)
