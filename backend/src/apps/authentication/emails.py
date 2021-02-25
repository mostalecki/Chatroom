from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from src.apps.authentication.models import EmailConfirmationToken
from src.celery import app


class EmailAddressConfirmationEmail(EmailMultiAlternatives):
    subject_text = "New Chatroom Account"
    txt_template = "authentication/email_address_confirmation_email.txt"
    html_template = "authentication/email_address_confirmation_email.html"

    def __init__(self, email_confirmation_token: str):
        token = EmailConfirmationToken.objects.select_related("user").get(
            key=email_confirmation_token
        )

        context = {
            "username": token.user.username,
            "token": token.key,
            "app_url": settings.APP_URL,
        }

        super().__init__(
            subject=self.subject_text,
            body=render_to_string(self.html_template, context),
            to=[token.user.email],
            alternatives=[(render_to_string(self.html_template, context), "text/html")],
        )


@app.task(name="src.apps.authentication.emails.send_email_address_confirmation_email")
def send_async_email_address_confirmation_email(email_confirmation_token: str) -> None:
    email = EmailAddressConfirmationEmail(email_confirmation_token)
    email.send()
