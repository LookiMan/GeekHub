import json

from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer

from chat.models import Chat, Message
from chat.serializers import MessageSerializer, ChatSerializer

from telegram_bot.tasks import async_send_text_message_to_client


class ChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    lookup_field = "ucid"

    @action()
    async def join_to_chats(self, **kwargs):
        await self.add_group("chat")

    @action()
    async def send_text_message(self, message, **kwargs):
        chat = await self.get_chat(pk=kwargs["ucid"])
        staff = self.scope["user"]
        await async_send_text_message_to_client(chat, message, staff)

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
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    @ database_sync_to_async
    def get_chat(self, pk: int) -> Chat:
        return Chat.objects.get(pk=pk)

    async def notify_staff(self, event):
        data = {
            "action": "create_new_chat",
            "telegram_chat_id": event["chat_id"],
        }
        await self.send(text_data=json.dumps(data))
