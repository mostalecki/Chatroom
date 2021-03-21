from django.urls import re_path

from src.apps.chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\w+)", consumers.ChatConsumer.as_asgi()),
]
