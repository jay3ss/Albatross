from unittest.mock import MagicMock, patch

from app import mail
from app.auth.email import send_email


@patch.object(mail, "send")
def test_send_email(mock_send):
    subject = "Test Email Subject"
    sender = "sender@example.com"
    recipients = ["recipient1@example.com", "recipient2@example.com"]
    text_body = "This is a test email in plain text format."
    html_body = "<p>This is a test email in HTML format.</p>"

    send_email(subject, sender, recipients, text_body, html_body)

    # Check that the message object was created with the correct attributes
    mock_send.assert_called_once()
    _, kwargs = mock_send.call_args
    message = kwargs["message"]
    assert message.subject == subject
    assert message.sender == sender
    assert message.recipients == recipients
    assert message.body == text_body
    assert message.html == html_body


if __name__ == "__main__":
    import pytest
    pytest.main(["-s", __file__])
