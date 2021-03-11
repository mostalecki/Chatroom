from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from ipware import get_client_ip

from src.utils.mixins import ExceptionHandlerMixin
from src.apps.ws_authentication.services import create_ticket
from src.apps.ws_authentication.serializers import TicketSerializer


class TicketCreateView(ExceptionHandlerMixin, CreateAPIView):
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        ticket = create_ticket(request.user, get_client_ip(request))

        return Response(data=self.serializer_class(ticket), status=status.HTTP_201_CREATED)
