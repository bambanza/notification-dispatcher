from core.dispatcher import dispatcher
from core.models import EmailMessage, SMSMessage

email_result = dispatcher.email(
    EmailMessage(
        to=["user@example.com"],
        subject="Notification Dispatcher Test",
        template="email/welcome.html",
        context={"name": "Emmanuel"},
    )
)

sms_result = dispatcher.sms(
    SMSMessage(
        to="+250700000000",
        message="Notification dispatcher test",
    )
)

print("Email task:", email_result.id)
print("SMS task:", sms_result.id)
