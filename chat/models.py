from django.db import models

# Create your models here.

class Connection(models.Model):
    ''' Stores information about websocket connected to a Room instance '''

    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    @property
    def is_unique(self):
        ''' Checks if it is user's only connection to this room '''
        if Connection.objects.filter(room=self.room, username=self.username).count() == 1:
            return True
        return False


class Room(models.Model):
    ''' Used to keep track of websocket connections in the same group '''

    name = models.CharField(max_length=128, unique=True)
    is_private = models.BooleanField(default=False)
    
    @property
    def num_of_connections(self):
        return Connection.objects.filter(room=self).values('username').distinct().count()

    @property
    def is_empty(self):
        if self.num_of_connections == 0:
            return True
        return False

    def __str__(self):
        return self.name
