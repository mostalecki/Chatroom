from src.apps.authentication.models import User
from src.apps.chat.models import Room
from src.apps.ws_authentication.services import create_ticket


def room_create(*, owner: User, is_private: bool, password: str = None) -> Room:
    room = Room(owner=owner, is_private=is_private)

    if password:
        room.set_password(password)

    room.save()

    return room
