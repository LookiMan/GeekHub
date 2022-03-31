from rest_framework import serializers

from chat.models import Staff


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ("id", "username", "first_name", "last_name")
