"""
Module for email-related functionality. The following environment variables need
to be set in order to send emails:

- MAIL_SERVER
- MAIL_PORT
- MAIL_USE_TLS
- MAIL_USERNAME
- MAIL_PASSWORD
"""
from flask_mail import Message

from app import mail


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
