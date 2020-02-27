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

        # Broadcast join message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_message',
                'user': self.username
            })
        await self.accept()

    async def disconnect(self, close_code):
        ''' Disconnects websocket and removes it from the group '''

        # Send leave message
        # Is only sent if leaving user is anonymous, or it is user's last instance in this room
        user = self.scope['user']
        if user.is_anonymous or self.is_connection_unique:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave_message',
                'user': self.username
            })
            
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
        ''' Receives message from room group, then forwards to websocket '''

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

    async def leave_message(self, event):
        ''' Receives user leaving notification from group and forwards it to websocket '''
        
        await self.send(text_data=json.dumps({
                'type': 'leave_message',
                'user': event['user'],
            }))

    async def join_message(self, event):
        ''' Receives user join notification from group and forwards it to websocket '''

        await self.send(text_data=json.dumps({
                'type': 'join_message',
                'user': event['user'],
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
    @database_sync_to_async
    def is_connection_unique(self):
        ''' Helper method for accessing Connection.is_unique from async piece of code'''
        return Connection.objects.get(channel_name=self.channel_name).is_unique

    @property
    def username(self):
        ''' Return authenticated user's username, or anonymous user's username with id stored in session '''

        user = self.scope['user']
        if user.is_authenticated:
            return user.username
        else:
            return f"{str(user)}#{self.scope['session']['id']}"