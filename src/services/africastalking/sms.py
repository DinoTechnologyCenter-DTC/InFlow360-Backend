"""Africastalking SMS service."""

from typing import Union

import africastalking
from pydantic import BaseModel

from src.settings import settings
from src.utils import phone_number_validator

africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)


class SMSResponse(BaseModel):
    """SMS response model."""

    cost: str
    number: str
    status: str
    messageId: Union[str, None] = None
    statusCode: int


class AfricasTalkingSMS:
    """AfricasTalking SMS service."""

    def __init__(self) -> None:
        """Initialize."""
        self.sms = africastalking.SMS

    def send_sms(self, to: Union[str, list], message: str) -> list[SMSResponse]:
        """Send an SMS message."""
        try:
            if isinstance(to, str):
                to = [phone_number_validator(to)]
            else:
                to = [phone_number_validator(num) for num in to]
        except Exception as error:
            msg = "Invalid phone number"
            raise ValueError(msg) from error

        response = self.sms.send(
            message,
            to,
            sender_id=settings.AT_SENDER_ID,
        )  # extra info
        recipients = response.get("SMSMessageData", {}).get("Recipients", [])
        # response should be recipients-> {cost, number and status and statusCode}
        return [
            SMSResponse(
                cost=recipient.get("cost"),
                number=recipient.get("number"),
                status=recipient.get("status"),
                statusCode=recipient.get("statusCode"),
                messageId=recipient.get("messageId"),
            )
            for recipient in recipients
        ]


africastalking_sms = AfricasTalkingSMS()
