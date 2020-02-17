from django.db import models

# Create your models here.

class Connection(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)

class Room(models.Model):
    name = models.CharField(max_length=128)
    is_private = models.BooleanField(default=False)
    
    @property
    def num_of_connections(self):
        return Connection.objects.filter(room=self).count()

    def __str__(self):
        return self.name
