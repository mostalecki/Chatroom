from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Connection
import json
import hashlib

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Assign user an id, if anonymous, and store it in session
        # id is first 4 digits of md5 hash of channel name
        user = self.scope['user']
        if user.is_authenticated is False:
            id = hashlib.md5()
            id.update(self.channel_name.split('.')[1].encode('utf-8'))
            self.scope['session']['id'] = str(int(id.hexdigest(),16))[0:4]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.connect_to_room(self.room_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.remove_connection(self.room_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        user = self.scope['user']
        if user.is_authenticated:
            username = user.username
        else:
            username = f"{str(user)}#{self.scope['session']['id']}"

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel': self.channel_name,
                'user': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        # type depends on wheter it's your message or it's from other channel
        if self.channel_name == event['sender_channel']:
            await self.send(text_data=json.dumps({
                'type': 'message_confirmation',
                'message': message
            }))
        else:
            await self.send(text_data=json.dumps({
                'type': 'message',
                'user': event['user'],
                'message': message
            }))

    @database_sync_to_async
    def connect_to_room(self, room_name, channel_name):
        room, created = Room.objects.get_or_create(name=self.room_name)
        connection = Connection(room=room, channel_name=self.channel_name)
        connection.save()

    @database_sync_to_async
    def remove_connection(self, room_name):
        Connection.objects.get(channel_name=self.channel_name).delete()
        self.remove_room_if_empty(room_name)

    def remove_room_if_empty(self, room_name):
        room = Room.objects.get(name=room_name)
        if Connection.objects.filter(room=room).count() == 0:
            room.delete()
