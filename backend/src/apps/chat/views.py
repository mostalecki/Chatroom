from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from src.apps.chat.models import Room
from src.apps.chat.serializers import (
    RoomSerializer,
    RoomCreateInputSerializer,
    RoomCreateOutputSerializer,
)
from src.utils.mixins import ExceptionHandlerMixin
from src.apps.chat.services import room_create


class RoomViewSet(
    ExceptionHandlerMixin,
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = (
        Room.objects.select_related("owner").with_user_count().order_by("-users_count")
    )
    permission_classes = (AllowAny,)
    serializer_class = RoomSerializer
    pagination_class = LimitOffsetPagination

    def filter_queryset(self, queryset):
        if self.action == "list":
            queryset = queryset.filter(is_private=False, is_active=True)
        return super().filter_queryset(queryset)

    @swagger_auto_schema(
        request_body=RoomCreateInputSerializer,
        responses={status.HTTP_201_CREATED: RoomCreateOutputSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = RoomCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner = request.user if request.user.is_authenticated else None

        room = room_create(**serializer.validated_data, owner=owner)

        return Response(
            data=RoomCreateOutputSerializer(room).data, status=status.HTTP_201_CREATED
        )
