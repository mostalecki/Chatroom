from rest_framework import serializers


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
