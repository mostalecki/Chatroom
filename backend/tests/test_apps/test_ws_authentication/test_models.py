import datetime

import pytest
from freezegun import freeze_time

from tests.factories import TicketFactory


@freeze_time("2021-02-25 00:01:01")
@pytest.mark.django_db
def test_ticket_is_expired():
    ticket = TicketFactory()

    assert ticket.is_expired is False

    # Reassign ticket creation date to 1 minute prior
    ticket.created_at = datetime.datetime(2021, 2, 25, 0, 0, 0)
    ticket.save()
    ticket.refresh_from_db()

    assert ticket.is_expired is True
