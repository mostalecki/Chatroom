import uuid
from hashlib import sha256
from django.db import models
from src.apps.authentication.models import User

# Create your models here.


class Connection(models.Model):
    """ Stores information about websocket connected to a Room instance """

    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    is_user_authenticated = models.BooleanField(default=False)

    # Following fields are used while displaying the message coming from this connection
    username = models.CharField(max_length=255)
    user_avatar_url = models.CharField(max_length=255, default="avatars/default.png")

    @property
    def is_unique(self):
        """ Checks if it is user's only connection to this room """
        if (
            Connection.objects.filter(room=self.room, username=self.username).count()
            == 1
        ):
            return True
        return False

    def save(self, *args, **kwargs):
        """ If user is authenticated, fetch his avatar's url from his UserProfile"""
        if self.is_user_authenticated:
            self.user_avatar_url = UserProfile.objects.get(
                user__username=self.username
            ).avatar.url
        super(Connection, self).save(*args, **kwargs)


class Room(models.Model):
    """ Used to keep track of websocket connections in the same group """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="rooms", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True)

    @property
    def num_of_connections(self):
        """ Returns amount of connections unique per username """
        return (
            Connection.objects.filter(room=self).values("username").distinct().count()
        )

    @property
    def user_list(self):
        return (
            Connection.objects.filter(room=self)
            .distinct("username")
            .values("is_user_authenticated", "username", "user_avatar_url")
        )

    @property
    def is_empty(self):
        if self.num_of_connections == 0:
            return True
        return False

    def set_password(self, password_str):
        # Room name is used as salt
        self.password = sha256((password_str + self.name).encode("utf-8'")).hexdigest()

    def __str__(self):
        return self.name
