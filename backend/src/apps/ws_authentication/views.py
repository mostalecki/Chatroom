from ipware import get_client_ip
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from src.apps.ws_authentication.serializers import TicketSerializer
from src.apps.ws_authentication.services import create_ticket
from src.utils.mixins import ExceptionHandlerMixin


class TicketCreateView(ExceptionHandlerMixin, CreateAPIView):
    serializer_class = TicketSerializer

    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request)[0]
        ticket = create_ticket(user=request.user, ip_address=client_ip)

        return Response(
            data=self.serializer_class(ticket).data, status=status.HTTP_201_CREATED
        )
