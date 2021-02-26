# Source: https://github.com/HackSoftware/Django-Styleguide
from django.core.exceptions import ValidationError

from rest_framework import exceptions as rest_exceptions


def _get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def _get_error_message(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    error_msg = _get_first_matching_attr(exc, "message", "messages")

    if isinstance(error_msg, list):
        error_msg = ", ".join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg


class ExceptionHandlerMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    """

    exception_mappings = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.exception_mappings.keys())):
            drf_exception_class = self.exception_mappings[exc.__class__]
            drf_exception = drf_exception_class(_get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
