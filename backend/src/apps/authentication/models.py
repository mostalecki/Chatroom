from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone

from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("User must have a username.")

        if email is None:
            raise TypeError("User must have an email address.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        if username is None:
            raise TypeError("User must have a username.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()


class EmailConfirmationToken(Token):
    user = models.OneToOneField(User, related_name="email_confirmation_token", on_delete=models.CASCADE)

    @property
    def is_expired(self) -> bool:
        return self.created < timezone.now() - timezone.timedelta(days=1)
