import uuid

import pytest
from channels.exceptions import DenyConnection

from src.apps.ws_authentication.services import ws_authenticate
from tests.factories import TicketFactory


@pytest.mark.django_db
def test_ws_authenticate():
    ticket = TicketFactory()
    user = ws_authenticate(token=ticket.token, ip_address=ticket.ip_address)

    assert ticket.user == user


@pytest.mark.django_db
def test_ws_authenticate_ticket_not_found():
    with pytest.raises(DenyConnection):
        ws_authenticate(token=str(uuid.uuid4()), ip_address="192.168.0.1")


@pytest.mark.django_db
def test_ws_authenticate_ip_addresses_not_matched():
    with pytest.raises(DenyConnection):
        ticket = TicketFactory(ip_address="192.168.0.1")

        ws_authenticate(token=ticket.token, ip_address="192.168.0.2")
