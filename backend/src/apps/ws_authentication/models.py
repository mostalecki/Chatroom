import uuid

from django.db import models
from django.utils import timezone

from src.apps.authentication.models import User


class Ticket(models.Model):
    user = models.ForeignKey(User, related_name="websocket_tickets")
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField()

    @property
    def is_expired(self) -> bool:
        return self.created < timezone.now() - timezone.timedelta(minutes=1)
