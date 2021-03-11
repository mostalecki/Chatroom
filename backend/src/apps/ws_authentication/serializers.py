from rest_framework import serializers

from src.apps.ws_authentication.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("token",)
