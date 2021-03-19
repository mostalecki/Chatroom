from channels.routing import ProtocolTypeRouter, URLRouter

import src.apps.chat.routing
from src.apps.ws_authentication.middleware import TicketAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": TicketAuthMiddlewareStack(
            URLRouter(src.apps.chat.routing.websocket_urlpatterns)
        ),
    }
)
