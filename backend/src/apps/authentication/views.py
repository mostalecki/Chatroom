from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from src.apps.authentication.services import user_register
from src.apps.authentication.serializers import UserRegisterSerializer
from src.utils.mixins import ExceptionHandlerMixin


class UserRegisterAPIView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_register(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
