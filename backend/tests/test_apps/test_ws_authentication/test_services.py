import datetime
import uuid

import pytest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from freezegun import freeze_time

from src.apps.ws_authentication.services import ws_authenticate
from tests.factories import TicketFactory


@pytest.mark.django_db
def test_ws_authenticate():
    ticket = TicketFactory()
    user = ws_authenticate(token=ticket.token, ip_address=ticket.ip_address)

    assert ticket.user == user


@pytest.mark.django_db
def test_ws_authenticate_ticket_not_found():
    with pytest.raises(ObjectDoesNotExist):
        ws_authenticate(token=str(uuid.uuid4()), ip_address="192.168.0.1")


@pytest.mark.django_db
def test_ws_authenticate_ip_addresses_not_matched():
    with pytest.raises(ValidationError):
        ticket = TicketFactory(ip_address="192.168.0.1")

        ws_authenticate(token=ticket.token, ip_address="192.168.0.2")


@freeze_time("2021-03-19 00:01:01")
@pytest.mark.django_db
def test_ws_authenticate_ticket_expired():
    with pytest.raises(ValidationError):
        ticket = TicketFactory(ip_address="192.168.0.1")

        # Reassign ticket creation date to 1 minute prior
        ticket.created_at = datetime.datetime(2021, 2, 25, 0, 0, 0)
        ticket.save()
        ticket.refresh_from_db()

        ws_authenticate(token=ticket.token, ip_address="192.168.0.2")
