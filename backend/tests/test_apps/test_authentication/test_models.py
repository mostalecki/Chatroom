import datetime

import pytest
from freezegun import freeze_time

from tests.factories import EmailConfirmationTokenFactory


@freeze_time("2021-02-25")
@pytest.mark.django_db
def test_email_confirmation_token_is_expired():
    token = EmailConfirmationTokenFactory()

    assert token.is_expired is False

    # Reassign token creation date to 2 days prior
    token.created = datetime.datetime(2021, 2, 23)
    token.save()
    token.refresh_from_db()

    assert token.is_expired is True
