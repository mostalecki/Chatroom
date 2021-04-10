import random

import factory.fuzzy
import factory
import faker

from src.apps.authentication.models import User, EmailConfirmationToken
from src.apps.chat.models import Room, Connection
from src.apps.profile.models import Profile
from src.apps.ws_authentication.models import Ticket
from tests.helpers import generate_channel_name, temporary_image_file

fake = faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"john{x}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.org")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    avatar = factory.fuzzy.FuzzyAttribute(temporary_image_file)


class EmailConfirmationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailConfirmationToken

    user = factory.SubFactory(UserFactory)


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    user = factory.SubFactory(UserFactory)
    ip_address = fake.ipv4()


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.fuzzy.FuzzyAttribute(lambda: f"Test Room #{random.randint(0, 1000)}")


class ConnectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Connection

    room = factory.SubFactory(RoomFactory)
    channel_name = factory.fuzzy.FuzzyAttribute(generate_channel_name)
