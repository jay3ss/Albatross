"""
Module for email-related functionality. The following environment variables need
to be set in order to send emails:

- MAIL_SERVER
- MAIL_PORT
- MAIL_USE_TLS
- MAIL_USERNAME
- MAIL_PASSWORD
"""
from flask import current_app, render_template
from flask_mail import Message

from app import mail, models


def send_email(subject: str, sender: str, recipients: list[str], text_body: str, html_body: str) -> None:
    """
    Send an email. The following environment variables need to be set in order to
    send emails:

    - MAIL_SERVER
    - MAIL_PORT
    - MAIL_USE_TLS
    - MAIL_USERNAME
    - MAIL_PASSWORD

    Args:
        subject (str): Email subject line
        sender (str): Sender's email
        recipients (list[str]): Email recipients' emails
        text_body (str): Body of the email's text
        html_body (str): Body of the email in HTML format
    """
    message = Message(subject=subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    mail.send(message=message)


def send_password_reset_email(user: models.User) -> None:
    """
    Sends the password reset email to the given user

    Args:
        user (models.User): The user whose password is being reset
    """
    token = user.get_reset_password_token()
    if current_app.config["DEBUG"]:
        rendered_email = render_template(
            "auth/emails/reset_password.html", token=token, user=user
        )
        print(rendered_email, flush=True)
    else:
        send_email(
            subject="[Albatross] Reset Your Password",
            sender=current_app.config["ADMINS"][0],
            recipients=[user.email],
            text_body=render_template(
                "auth/emails/reset_password.txt", token=token, user=user
            ),
            html_body=render_template(
                "auth/emails/reset_password.html", token=token, user=user
            ),
        )
