from django.contrib.auth.password_validation import validate_password

from src.apps.authentication.models import User


def user_register(*, email: str, username: str, password: str) -> User:
    validate_password(password)

    user = User(username=username, email=email)
    user.set_password(password)
    user.full_clean(exclude=["password"])
    user.save()

    # send email address verification message

    return user


def user_email_verify(*, email_verification_token: str) -> None:
    pass


def user_password_reset_request() -> None:
    pass


def user_password_reset(*, password_reset_token: str, new_password: str) -> None:
    pass
