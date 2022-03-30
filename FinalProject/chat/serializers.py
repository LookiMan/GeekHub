from rest_framework import serializers

from chat.models import Staff, Chat, Message
from telegram_bot.models import TelegramUser


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ("id", "username", "first_name", "last_name")


class ClientSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = ("id", "image_url", "first_name", "last_name", "username")

    def get_image_url(self, obj):
        return obj.image_url


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    staff = StaffSerializer()

    class Meta:
        model = Message
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    client = ClientSerializer()

    class Meta:
        model = Chat
        fields = ("ucid", "first_name", "client", "last_name",
                  "username", "messages", "last_message")
        depth = 1
        read_only_fields = ("messages", "last_message")

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data


class ChatSerializerWithoutMessages(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    client = ClientSerializer()

    class Meta:
        model = Chat
        fields = ("ucid", "first_name", "client", "last_name",
                  "username", "last_message")
        depth = 1
        read_only_fields = ("last_message")

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data
