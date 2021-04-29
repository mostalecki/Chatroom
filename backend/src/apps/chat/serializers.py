from rest_framework import serializers

from src.apps.authentication.models import User
from src.apps.chat.models import Room


class RoomOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class RoomSerializer(serializers.ModelSerializer):
    users_count = serializers.IntegerField()
    owner = RoomOwnerSerializer()

    class Meta:
        model = Room
        fields = ("id", "name", "owner", "users_count", "is_password_protected")


class RoomCreateOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "is_private", "is_password_protected")


class RoomCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("name", "is_private", "password")
