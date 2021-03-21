from src.apps.authentication.models import User
from src.apps.chat.models import Room


def room_create(*, name: str, is_private: bool, password: str = None, owner: User = None) -> Room:
    room = Room(name=name, is_private=is_private)

    if owner:
        room.owner = owner

    if password:
        room.set_password(password)

    room.save()

    return room
