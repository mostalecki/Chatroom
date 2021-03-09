from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from src.apps.authentication import views

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/register", views.UserRegisterAPIView.as_view(), name="user_register"),
    path(
        "users/email-confirm",
        views.UserEmailConfirmationView.as_view(),
        name="user_email_confirm",
    ),
    path(
        "users/resend-activation-email",
        views.UserResendEmailConfirmationView.as_view(),
        name="user_email_confirm",
    ),
    path("users/me", views.UserRetrieveView.as_view(), name="user_retrieve")
]
