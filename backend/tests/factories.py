import factory
import faker

from src.apps.authentication.models import User, EmailConfirmationToken
from src.apps.ws_authentication.models import Ticket

fake = faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"john{x}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.org")


class EmailConfirmationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailConfirmationToken

    user = factory.SubFactory(UserFactory)


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    user = factory.SubFactory(UserFactory)
    ip_address = fake.ipv4()
