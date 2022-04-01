from rest_framework import serializers

from chat.serializers import StaffSerializer
from telegram_bot.models import User, Chat, Message


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("uuid", "id", "first_name", "last_name", "username", "image")


class MessageSerializer(serializers.ModelSerializer):
    staff = StaffSerializer()

    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "umid", "id", "chat", "user", "staff", "reply_to_message",
            "text", "photo", "document", "file_name", "caption",
            "created_at_formatted"
        )
        depth = 2

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = ClientSerializer()
    staff = StaffSerializer()

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "ucid", "first_name", "last_name", "username",
            "user", "staff", "messages", "last_message",
        )
        depth = 1
        read_only_fields = ("messages", "last_message")

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data


class ChatSerializerWithoutMessages(serializers.ModelSerializer):
    client = ClientSerializer()

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ("ucid", "first_name", "client", "last_name",
                  "username", "last_message")
        depth = 1
        read_only_fields = ("last_message")

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data
