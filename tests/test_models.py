from core.models import EmailMessage, SMSMessage


def test_email_message():
    msg = EmailMessage(
        to=["user@example.com"],
        subject="Hello",
        text_body="Hello there",
    )
    assert str(msg.to[0]) == "user@example.com"


def test_sms_message():
    msg = SMSMessage(
        to="+250700000000",
        message="Hello",
    )
    assert msg.message == "Hello"
