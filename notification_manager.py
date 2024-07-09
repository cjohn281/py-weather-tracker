from twilio.rest import Client
from dotenv import load_dotenv
import os
import smtplib

load_dotenv()


class NotificationManager:
    """A Class designed to interact with the Twilio API and send text messages through the Twilio service"""
    def __init__(self):
        self._source_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self._dest_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        self.twilio_client = Client(os.environ.get("TWILIO_SID"),
                                    os.environ.get("TWILIO_AUTH_TOKEN"))
        self.smtp = smtplib.SMTP(host=os.environ.get("SMTP"))
        self.smtp.starttls()

    def send_message(self, message_body: str):
        """Sends messages using the Twilio service

        :parameter message_body: The body of the message to send via text message"""
        self.twilio_client.messages.create(
            from_=self._source_number,
            to=self._dest_number,
            body=message_body
        )

    def send_email(self, message_body: str):
        """Sends emails using smtplib

        :parameter message_body: The body of the message to send via email"""
        user = os.environ.get("EMAIL_USER")
        self.smtp.login(user=user, password=os.environ.get("EMAIL_PASSWORD"))
        self.smtp.sendmail(
            to_addrs=os.environ.get("TO_EMAIL"),
            from_addr=user,
            msg=f"Subject: Weather Alert!\n\n{message_body}"
        )
