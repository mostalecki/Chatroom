from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from src.apps.chat.models import Room
from src.apps.chat.serializers import RoomSerializer, RoomCreateSerializer
from src.utils.mixins import ExceptionHandlerMixin
from src.apps.chat.services import room_create


class RoomViewSet(ExceptionHandlerMixin, GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin):
    queryset = Room.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RoomSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return RoomCreateSerializer
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        if self.action == "list":
            queryset = queryset.filter(is_private=False)
        return super().filter_queryset(queryset)

    @swagger_auto_schema(
        request_body=RoomCreateSerializer,
        responses={status.HTTP_201_CREATED: RoomSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)

        room = room_create(**serializer.validated_data)

        return Response(data=RoomSerializer(room).data, status=status.HTTP_201_CREATED)
