from uuid import uuid4

import json
import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist

from src.apps.chat.models import Room
from tests.factories import RoomFactory, ConnectionFactory


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_connect_username_not_specified(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()
    communicator = WebsocketCommunicator(chat_consumer_application, f"ws/chat/{room.id}")
    communicator.scope["user"] = AnonymousUser()
    connected, close_code = await communicator.connect()

    assert connected is False
    assert close_code == 4000


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_connect_room_does_not_exist(chat_consumer_application):
    non_existing_room_id = uuid4()
    communicator = WebsocketCommunicator(chat_consumer_application, f"ws/chat/{non_existing_room_id}?username={'test'}")
    communicator.scope["user"] = AnonymousUser()
    connected, close_code = await communicator.connect()

    assert connected is False
    assert close_code == 4001


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_connect_invalid_room_password(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()
    await database_sync_to_async(room.set_password)("validPassword")
    await database_sync_to_async(room.save)()

    communicator = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'test'}&password={'invalidPassword'}"
    )
    communicator.scope["user"] = AnonymousUser()
    connected, close_code = await communicator.connect()

    assert connected is False
    assert close_code == 4002


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_connect_returns_user_list(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()
    # Create dummy connections
    await database_sync_to_async(ConnectionFactory.create_batch)(9, room=room)

    communicator = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'test'}"
    )
    communicator.scope["user"] = AnonymousUser()
    connected, subprotocol = await communicator.connect()

    response = await communicator.receive_from()
    response = json.loads(response)

    assert connected is True
    assert response["type"] == "user_list"
    assert len(response["users"]) == 10

    await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_send_join_leave_messages(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()

    # First connection
    communicator1 = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'testUser1'}"
    )
    communicator1.scope["user"] = AnonymousUser()
    await communicator1.connect()
    # Receive first connection's user list message and self-join message
    await communicator1.receive_from()
    await communicator1.receive_from()

    # Second connection
    communicator2 = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'testUser2'}"
    )
    communicator2.scope["user"] = AnonymousUser()

    # Await communicator2 join message on communicator1
    await communicator2.connect()
    response1 = await communicator1.receive_json_from()
    assert response1["type"] == "join_message"
    assert response1["username"] == "testUser2"

    # Send message from communicator2 and await it on communicator1
    await communicator2.send_json_to({"message": "hello"})
    response2 = await communicator1.receive_json_from()
    assert response2["type"] == "message"
    assert response2["message"] == "hello"

    # Await communicator2 leave message on communicator1
    await communicator2.disconnect()
    response3 = await communicator1.receive_json_from()
    assert response3["type"] == "leave_message"
    assert response3["username"] == "testUser2"

    await communicator1.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_activates_room(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()

    communicator = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'testUser1'}"
    )
    communicator.scope["user"] = AnonymousUser()
    await communicator.connect()
    await database_sync_to_async(room.refresh_from_db)()

    assert room.is_active is True


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_chat_consumer_remove_empty_room(chat_consumer_application):
    room = await database_sync_to_async(RoomFactory)()

    communicator = WebsocketCommunicator(
        chat_consumer_application,
        f"ws/chat/{room.id}?username={'testUser1'}"
    )
    communicator.scope["user"] = AnonymousUser()
    await communicator.connect()
    await communicator.disconnect()

    with pytest.raises(ObjectDoesNotExist):
        await database_sync_to_async(Room.objects.get)(pk=room.id)
