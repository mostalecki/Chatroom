from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from src.apps.authentication.services import user_register, user_email_verify, user_resend_activation_email
from src.apps.authentication.serializers import UserRegisterSerializer, TokenSerializer, EmailSerializer
from src.utils.mixins import ExceptionHandlerMixin


class UserRegisterAPIView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_register(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserEmailConfirmationView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email_verify(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class UserResendEmailConfirmationView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_resend_activation_email(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

