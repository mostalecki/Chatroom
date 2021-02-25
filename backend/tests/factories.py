import factory

from src.apps.authentication.models import User, EmailConfirmationToken


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f"john{x}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.org")


class EmailConfirmationTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailConfirmationToken

    user = factory.SubFactory(UserFactory)
