import pytest
from channels.routing import URLRouter
from django.conf import settings
from src.apps.chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns


def pytest_configure():
    settings.CHANNEL_LAYERS["default"]["BACKEND"] = "channels.layers.InMemoryChannelLayer"
    settings.CHANNEL_LAYERS["default"]["CONFIG"].pop("hosts")


@pytest.fixture()
def celery_task_eager():
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture()
def chat_consumer_application():
    return URLRouter(chat_websocket_urlpatterns)
