from twilio.rest import Client
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()


class NotificationManager:
    """This class is responsible for communicating with Twilio and AMTP services
    and sending messages via SMS and email.
    """
    def __init__(self):
        self._source_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self._dest_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.twilio_client = Client(os.environ.get("TWILIO_SID"),
                                    os.environ.get("TWILIO_AUTH_TOKEN"))
        self.smtp = smtplib.SMTP(host=os.environ.get("SMTP"))
        self.smtp.starttls()

    def send_message(self, message_body: str):
        """Sends SMS messages via Twilio service

        Args:
            message_body (str): The content of the message to be sent via SMS
        """
        self.twilio_client.messages.create(
            from_=self._source_number,
            to=self._dest_number,
            body=message_body
        )

    def send_email(self, message_body: str):
        """Sends email messages wia smtplib

        Args:
            message_body (str): The content of the message to be sent via email
        """
        user = os.environ.get("EMAIL_USER")
        self.smtp.login(user=user, password=os.environ.get("EMAIL_PASSWORD"))
        self.smtp.sendmail(
            to_addrs=os.environ.get("TO_EMAIL"),
            from_addr=user,
            msg=f"Subject: Weather Alert!\n\n{message_body}"
        )
