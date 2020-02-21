from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')