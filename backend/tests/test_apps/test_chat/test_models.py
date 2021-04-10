import pytest

from tests.factories import RoomFactory, ConnectionFactory, UserFactory, ProfileFactory


@pytest.mark.django_db
def test_anonymous_connection_is_unique():
    room = RoomFactory()
    user = UserFactory(username="testUser")

    conn = ConnectionFactory(room=room, username="testUser")
    # Create second anonymous connection and authenticated connection with the same username
    ConnectionFactory(room=room, username="testUser")
    ConnectionFactory(room=room, username=user.username, is_user_authenticated=True)

    # First connection should still be unique
    assert conn.is_unique is True


@pytest.mark.django_db
def test_connection_is_unique():
    room = RoomFactory()
    user = UserFactory(username="testUser")

    conn = ConnectionFactory(room=room, username=user.username, is_user_authenticated=True)
    # Create a bunch of anonymous connections with the same username
    ConnectionFactory.create_batch(5, room=room, username=user.username)

    # First connection should still be unique
    assert conn.is_unique is True


@pytest.mark.django_db
def test_connection_is_not_unique():
    room = RoomFactory()
    user = UserFactory(username="testUser")

    conns = ConnectionFactory.create_batch(2, room=room, username=user.username, is_user_authenticated=True)

    assert conns[0].is_unique is False


@pytest.mark.django_db
def test_connection_saves_user_avatar_url():
    profile = ProfileFactory()

    conn = ConnectionFactory(username=profile.user.username, is_user_authenticated=True)

    assert conn.user_avatar_url == profile.avatar.url


@pytest.mark.django_db
def test_room_num_of_connections():
    room = RoomFactory()
    users = UserFactory.create_batch(2)

    # Create some anonymous connections
    ConnectionFactory.create_batch(5, room=room)

    # Create multiple connections for the 2 of authenticated users
    ConnectionFactory.create_batch(3, room=room, username=users[0].username, is_user_authenticated=True)
    ConnectionFactory.create_batch(2, room=room, username=users[1].username, is_user_authenticated=True)

    # Total number of unique connections should equal to 7
    # (5 anonymous connections and 2 users with multiple connections)
    assert room.num_of_connections == 7


@pytest.mark.django_db
def test_room_users():
    room = RoomFactory()
    users = UserFactory.create_batch(2)

    anonymous_connections = ConnectionFactory.create_batch(10, room=room)
    user1_connections = ConnectionFactory.create_batch(2, room=room, username=users[0].username, is_user_authenticated=True)
    user2_connections = ConnectionFactory.create_batch(3, room=room, username=users[1].username,
                                                       is_user_authenticated=True)

    # `unique_connections` are expected to be all of the anonymous connections plus
    # the oldest connection for every authenticated user
    unique_connections = anonymous_connections
    unique_connections.extend((user1_connections[0], user2_connections[0]))

    assert list(room.users) == unique_connections


@pytest.mark.django_db
def test_room_validate_password():
    password = "123QWEASD"

    room = RoomFactory()
    room.set_password(password)

    assert room.validate_password(password) is True
