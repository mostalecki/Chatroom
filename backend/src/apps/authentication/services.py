from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from src.apps.authentication.models import User, EmailConfirmationToken
from src.apps.authentication.emails import send_async_email_address_confirmation_email
from src.celery import QueuePriority


@transaction.atomic
def user_register(*, email: str, username: str, password: str) -> User:
    validate_password(password)

    user = User(username=username, email=email)
    user.set_password(password)
    user.full_clean(exclude=["password"])
    user.save()

    email_confirmation_token = EmailConfirmationToken.objects.create(user=user)

    send_async_email_address_confirmation_email.apply_async(
        queue=QueuePriority.NORMAL,
        kwargs={"email_confirmation_token": email_confirmation_token.key}
    )

    return user


@transaction.atomic
def user_email_verify(*, token: str) -> None:
    email_verification_token = get_object_or_404(EmailConfirmationToken.objects.select_related(), key=token)

    if email_verification_token.is_expired:
        raise ValidationError("Token has expired")

    user = email_verification_token.user
    user.is_active = True
    user.save()

    email_verification_token.delete()


def user_resend_activation_email(*, email: str) -> None:
    user = get_object_or_404(User.objects.select_related("email_confirmation_token"), email=email)

    if user.email_confirmation_token is not None:
        user.email_confirmation_token.delete()

    email_confirmation_token = EmailConfirmationToken.objects.create(user=user)
    send_async_email_address_confirmation_email.apply_async(
        queue=QueuePriority.NORMAL,
        kwargs={"email_confirmation_token": email_confirmation_token.key}
    )


