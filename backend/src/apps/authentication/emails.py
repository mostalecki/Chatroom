from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from src.apps.authentication.models import EmailConfirmationToken
from src.celery import app


class EmailAddressConfirmationEmail(EmailMessage):
    subject_text = "New Chatroom Account"
    html_template = "authentication/email_address_confirmation_email.html"

    def __init__(self, email_confirmation_token: str):
        token = EmailConfirmationToken.objects.select_related("user").get(key=email_confirmation_token)

        context = {
            "username": token.user.username,
            "token": token.key
        }

        super().__init__(
            subject=self.subject_text,
            body=render_to_string(self.html_template, context),
            to=[token.user.email]

        )


@app.task(name="src.apps.authentication.emails.send_email_address_confirmation_email")
def send_async_email_address_confirmation_email(email_confirmation_token: str) -> None:
    email = EmailAddressConfirmationEmail(email_confirmation_token)
    email.send()
