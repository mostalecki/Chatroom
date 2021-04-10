import uuid

from django.db import models
from django.utils import timezone

from src.apps.authentication.models import User


class Ticket(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="websocket_tickets", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    @property
    def is_expired(self) -> bool:
        return self.created_at < timezone.now() - timezone.timedelta(minutes=1)
