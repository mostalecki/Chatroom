from django.db import models
from src.apps.authentication.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
