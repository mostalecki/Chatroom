import json
from typing import Union, Tuple

from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from src.apps.authentication.models import User
from src.apps.chat.models import Room, Connection
from src.utils.helpers import query_string_parser


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        # Create variables that will be assigned upon connection
        self.room_group_name = None
        self.room = None
        self.connection = None
        self.user = None

    async def connect(self):
        """ Create new websocket connection, connect to the group
            and assign id if user is anonymous """
        query_params = query_string_parser(self.scope["query_string"])

        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{room_id}"

        self.user = self.scope["user"]

        if self.user.is_anonymous:
            # Set username to value passed in query param
            # If it's not present - deny connection
            if "username" in query_params:
                self.user.username = query_params["username"]
            else:
                raise DenyConnection("Anonymous users must provide username")

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.room, self.connection = self.connect_to_room(self.user)

        # Broadcast join message to group
        if self.user.is_anonymous or self.is_connection_unique:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "join_message",
                    "username": self.user.username,
                    "user_avatar_url": self.connection.user_avatar_url,
                },
            )

        await self.accept()

        # Send back list of profile currently in room
        await self.send(
            text_data=json.dumps({"type": "user_list", "users": self.user_list})
        )

    async def disconnect(self, close_code):
        """ Disconnects websocket and removes it from the group """
        #TODO: refactor

        # Send leave message
        # Is only sent if leaving user is anonymous, or it is user's last instance in this room
        if self.user.is_anonymous or self.is_connection_unique:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "leave_message", "username": self.user.username},
            )

        # Leave room group
        self.remove_connection()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """ Receive messsage from websocket and forward it to the group """

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_channel": self.channel_name,
                "user": self.username,
            },
        )

    async def chat_message(self, event):
        """ Receives message from room group, then forwards to websocket """

        message = event["message"]
        # Send message to WebSocket
        # type depends on wheter it's from this particular channel (then it's message_confirmation)
        # or if it's from other channel (message)
        if self.channel_name == event["sender_channel"]:
            await self.send(
                text_data=json.dumps(
                    {"type": "message_confirmation", "message": message}
                )
            )
        else:
            await self.send(
                text_data=json.dumps(
                    {"type": "message", "user": event["user"], "message": message}
                )
            )

    async def leave_message(self, event):
        """ Receives user leaving notification from group and forwards it to websocket """

        await self.send(
            text_data=json.dumps(
                {"type": "leave_message", "username": event["username"]}
            )
        )

    async def join_message(self, event):
        """ Receives user join notification from group and forwards it to websocket """

        await self.send(
            text_data=json.dumps(
                {
                    "type": "join_message",
                    "username": event["username"],
                    "user_avatar_url": event["user_avatar_url"],
                }
            )
        )

    @database_sync_to_async
    def connect_to_room(self, user: Union[User, AnonymousUser]) -> Tuple[Room, Connection]:
        """ Creates/gets new instance of Room object and creates new Connection with reference to it"""

        room, created = Room.objects.get_or_create(name=self.room_group_name)
        connection = Connection(
            room=room,
            channel_name=self.channel_name,
            username=user.username,
            is_user_authenticated=user.is_authenticated,
        )
        connection.save()

        return room, connection

    @database_sync_to_async
    def remove_connection(self) -> None:
        """ Removes connection to room, removes room if empty """

        self.connection.delete()
        if self.room.is_empty:
            self.room.delete()

    @property
    @database_sync_to_async
    def is_connection_unique(self) -> bool:
        return self.connection.is_unique

    @property
    @database_sync_to_async
    def user_list(self):
        """ List of users currently in this room """

        return list(self.room.user_list)
