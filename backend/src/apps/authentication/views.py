from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from src.apps.authentication.serializers import (
    UserRegisterSerializer,
    TokenSerializer,
    EmailSerializer,
    UserSerializer,
)
from src.apps.authentication.services import (
    user_register,
    user_email_verify,
    user_resend_activation_email,
)
from src.utils.mixins import ExceptionHandlerMixin


class UserRegisterAPIView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        request_body=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="User created successfully, email address confirmation message was sent"
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_register(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class UserEmailConfirmationView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer

    @swagger_auto_schema(
        request_body=TokenSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Email confirmed successfully, user may now log in"
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email_verify(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class UserResendEmailConfirmationView(ExceptionHandlerMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailSerializer

    @swagger_auto_schema(
        request_body=EmailSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Your request was accepted, email message with new activation link was sent"
            )
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_resend_activation_email(**serializer.validated_data)

        return Response(status=status.HTTP_200_OK)


class UserRetrieveView(ExceptionHandlerMixin, RetrieveAPIView):
    """Retrieves current user info"""
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(status=status.HTTP_200_OK, data=serializer.data)
