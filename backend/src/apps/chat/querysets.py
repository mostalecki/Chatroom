from django.db.models import Q
from django.db.models.query import QuerySet


class ConnectionQuerySet(QuerySet):
    def unique_per_user_in_room(self, room: "Room"):
        """
        Returns connections for passed room that are unique in respect to user.
        Anonymous connections are all treated as unique.
        """
        anonymous_users_ids = self.filter(is_user_authenticated=False, room=room).only(
            "id"
        )
        authenticated_users_ids = (
            self.filter(is_user_authenticated=True, room=room)
            .distinct("username")
            .only("id")
        )

        anonymous_unique_connections = Q(id__in=anonymous_users_ids)
        authenticated_unique_connections = Q(id__in=authenticated_users_ids)

        return self.filter(
            anonymous_unique_connections | authenticated_unique_connections
        )
