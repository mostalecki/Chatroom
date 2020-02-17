from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Connection
import json
import hashlib

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        ''' Create new websocket connection, connect to the group and assign id if user is anonymus '''
        
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

        await self.connect_to_room(self.room_name, self.channel_name, self.username)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.remove_connection(self.room_name)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        ''' Receive messsage from websocket and forward it to the group '''

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel': self.channel_name,
                'user': self.username
            }
        )

    async def chat_message(self, event):
        ''' Receive message from room group, then send to websocket with information wheter it's sender's message '''

        message = event['message']
        # Send message to WebSocket
        # type depends on wheter it's from this particular channel (then it's message_confirmation)
        # or if it's from other channel (message)
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
    def connect_to_room(self, room_name, channel_name, username):
        ''' Creates/gets new instance of Room object and creates new Connection with reference to it'''

        room, created = Room.objects.get_or_create(name=self.room_name)
        connection = Connection(room=room, channel_name=self.channel_name, username=username)
        connection.save()

    @database_sync_to_async
    def remove_connection(self, room_name):
        ''' Removes connection to room, removes room if empty '''

        Connection.objects.get(channel_name=self.channel_name).delete()
        room = Room.objects.get(name=room_name)
        if room.is_empty:
            room.delete()

    @property
    def username(self):
        ''' Return authenticated user username, or anonymous user username with id stored in session '''

        user = self.scope['user']
        if user.is_authenticated:
            return user.username
        else:
            return f"{str(user)}#{self.scope['session']['id']}"
