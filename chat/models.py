from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=128)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Connection(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
