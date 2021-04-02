from typing import Union

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser

from src.apps.authentication.models import User
from src.apps.ws_authentication.services import ws_authenticate


@database_sync_to_async
def get_user(*, query_string: str, client_ip: str) -> Union[User, AnonymousUser]:
    try:
        query = dict((x.split("=") for x in query_string.decode().split("&")))
        token = query.get("token")
        return ws_authenticate(token=token, ip_address=client_ip)
    except:
        return AnonymousUser()


class TicketAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that authenticates user through one-time use connection ticket.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        client_ip = scope["client"][0]
        scope["user"] = await get_user(
            query_string=scope["query_string"], client_ip=client_ip
        )

        return await super().__call__(scope, receive, send)


def TicketAuthMiddlewareStack(inner):
    return TicketAuthMiddleware(AuthMiddlewareStack(inner))
