from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv
import os

load_dotenv()


class NotificationManager:
    """A Class designed to interact with the Twilio API and send text messages through the Twilio service"""
    def __init__(self):
        self._source_number = os.environ.get("TWILIO_VIRTUAL_NUMBER")
        self._dest_number = os.environ.get("TWILIO_VERIFIED_NUMBER")
        # self._proxy_client = TwilioHttpClient(proxy={"http": os.environ["http_proxy"], "https": os.environ["https_proxy"]})
        # self.twilio_client = Client(os.environ.get("TWILIO_SID"),
        #                             os.environ.get("TWILIO_AUTH_TOKEN"),
        #                             http_client=self._proxy_client)
        self.twilio_client = Client(os.environ.get("TWILIO_SID"),
                                    os.environ.get("TWILIO_AUTH_TOKEN"))

    def send_message(self, message_body: str):
        """Sends messages using the Twilio service

        :parameter message_body: The body of the message to send via text message"""
        self.twilio_client.messages.create(
            from_=self._source_number,
            to=self._dest_number,
            body=message_body
        )
