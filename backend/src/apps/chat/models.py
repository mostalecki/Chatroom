import uuid
from hashlib import sha256

from django.db import models
from django.db.models import QuerySet

from src.apps.authentication.models import User
from src.apps.chat.querysets import ConnectionQuerySet


class Connection(models.Model):
    """ Stores information about websocket connected to a Room instance """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    is_user_authenticated = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    user_avatar_url = models.CharField(max_length=255, null=True)

    objects = ConnectionQuerySet.as_manager()

    @property
    def is_unique(self) -> bool:
        """ Checks if it is user's only connection to related room """
        if not self.is_user_authenticated:
            return True

        if (
            Connection.objects.filter(
                room=self.room, username=self.username, is_user_authenticated=True
            )
            .exclude(id=self.id)
            .exists()
        ):
            return False

        return True

    def save(self, *args, **kwargs):
        if not self.is_user_authenticated and not self.id:
            self.user_avatar_url = (
                User.objects.select_related("profile")
                .get(username=self.username)
                .profile.avatar.url
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} | {'Authenticated' if self.is_user_authenticated else 'Not authenticated'}"


class Room(models.Model):
    """ Used to keep track of websocket connections in the same group """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        User, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=128)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True)

    @property
    def num_of_connections(self) -> int:
        """ Returns amount of unique (with respect to user) connections in this room """
        return Connection.objects.unique_per_user_in_room(room=self).count()

    @property
    def users(self) -> QuerySet[Connection]:
        return Connection.objects.unique_per_user_in_room(room=self)

    @property
    def is_empty(self) -> bool:
        return self.num_of_connections == 0

    def set_password(self, password_str: str) -> None:
        # Room name is used as salt
        self.password = sha256((password_str + self.name).encode("utf-8'")).hexdigest()

    def __str__(self):
        return self.name
