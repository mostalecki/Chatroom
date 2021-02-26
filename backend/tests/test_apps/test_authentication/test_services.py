import datetime

import pytest
from django.core import mail
from freezegun import freeze_time

from src.apps.authentication.models import User, EmailConfirmationToken
from src.apps.authentication.services import (
    user_register,
    user_email_verify,
    user_resend_activation_email,
)
from src.apps.profile.models import Profile
from tests.factories import EmailConfirmationTokenFactory


@pytest.mark.django_db
def test_user_register(celery_task_eager):
    user = user_register(
        email="email@example.com", username="example_user", password="randomPassword"
    )

    assert user.is_active is False
    assert Profile.objects.filter(user=user).exists() is True
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_user_email_verify():
    token = EmailConfirmationTokenFactory()
    user_email_verify(token=token.key)

    assert EmailConfirmationToken.objects.filter(key=token.key).exists() is False
    assert User.objects.get(username=token.user.username).is_active is True


@freeze_time("2021-02-25")
@pytest.mark.django_db
def test_user_resend_activation_email(celery_task_eager):
    token = EmailConfirmationTokenFactory()

    # Reassign token creation date to 2 days prior
    token.created = datetime.datetime(2021, 2, 23)
    token.save()

    user_resend_activation_email(email=token.user.email)

    user = User.objects.select_related("email_confirmation_token").get(
        username=token.user.username
    )

    assert user.email_confirmation_token.is_expired is False
    assert user.email_confirmation_token.key != token.key
    assert len(mail.outbox) == 1
