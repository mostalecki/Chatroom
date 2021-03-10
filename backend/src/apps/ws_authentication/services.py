from channels.exceptions import DenyConnection

from src.apps.authentication.models import User
from src.apps.ws_authentication.models import Ticket


def create_ticket(user: User, ip_address: str) -> Ticket:
    return Ticket.objects.create(user=user, ip_address=ip_address)


def authenticate(token: str, ip_address) -> User:
    try:
        ticket = Ticket.objects.get(token=token)
    except Ticket.DoesNotExist:
        raise DenyConnection()

    if ticket.is_expired or ticket.ip_address != ip_address:
        raise DenyConnection()

    return ticket.user

