from django.test import TestCase
from .models import Room, Connection

# Create your tests here.

class ConnectionTestCase(TestCase):
    def setUp(self):
        room = Room.objects.create(name="testRoom")
        Connection.objects.create(room=room, channel_name='123', username='user1')
        Connection.objects.create(room=room, channel_name='456', username='user1')
        Connection.objects.create(room=room, channel_name='789', username='user2')

    def test_connection_is_unique(self):
        ''' Tests if it's the only connection in the room with tied to username'''
        connection1 = Connection.objects.get(channel_name='123')
        connection2 = Connection.objects.get(channel_name='456')
        connection3 = Connection.objects.get(channel_name='789')
        self.assertEqual(connection1.is_unique, False)
        self.assertEqual(connection2.is_unique, False)
        self.assertEqual(connection3.is_unique, True)


class RoomTestCase(TestCase):
    def setUp(self):
        room1 = Room.objects.create(name="testRoom1")
        room2 = Room.objects.create(name="testRoom2")
        Connection.objects.create(room=room1, channel_name='123', username='user1')
        Connection.objects.create(room=room1, channel_name='456', username='user1')
        Connection.objects.create(room=room1, channel_name='789', username='user2')

    def test_num_of_connections(self):
        ''' Tests the count of connections within the room with unique usernames '''
        room1 = Room.objects.get(name="testRoom1")
        room2 = Room.objects.get(name="testRoom2")
        self.assertEqual(room1.num_of_connections, 2)
        self.assertEqual(room2.num_of_connections, 0)

    def test_is_empty(self):
        room1 = Room.objects.get(name="testRoom1")
        room2 = Room.objects.get(name="testRoom2")
        self.assertEqual(room1.is_empty, False)
        self.assertEqual(room2.is_empty, True)
