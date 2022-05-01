from rest_framework import serializers

from telegram_bot.models import User


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "uuid", "id",
            "first_name", "last_name", "username",
            "image", "is_blocked"
        )
