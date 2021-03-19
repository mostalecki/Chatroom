from django.core.exceptions import ValidationError, ObjectDoesNotExist

from src.apps.authentication.models import User
from src.apps.ws_authentication.models import Ticket


def create_ticket(*, user: User, ip_address: str) -> Ticket:
    return Ticket.objects.create(user=user, ip_address=ip_address)


def ws_authenticate(*, token: str, ip_address) -> User:
    try:
        ticket = Ticket.objects.select_related("user").get(token=token)
    except Ticket.DoesNotExist:
        raise ObjectDoesNotExist()

    if ticket.is_expired or ticket.ip_address != ip_address:
        ticket.delete()
        raise ValidationError("Ticket has expired")

    if ticket.ip_address != ip_address:
        raise ValidationError("Client and ticket ip addresses do not match.")

    ticket.delete()

    return ticket.user

