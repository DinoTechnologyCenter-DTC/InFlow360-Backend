"""Africas talkning Routes."""

from fastapi import APIRouter, Request

from src.services.africastalking.sms import africastalking_sms
from src.services.africastalking.ussd import ussd_menu

router = APIRouter()


@router.post("/sms")
async def send_sms(request: Request) -> dict:
    """Handle Two way sms."""
    form_data = await request.form()
    to = form_data.get("from")
    message = form_data.get("text")

    message = (
        "Welcome Here\nWe are here to help you with invoicing. Please visit *384*21038#"
    )

    africastalking_sms.send_sms(to, message)

    return {"status": "success", "data": {"to": to, "message": message}}


@router.post("/ussd")
async def handle_ussd(request: Request) -> str:
    """Handle USSD Request."""
    form_data = await request.form()
    text = form_data.get("text", "default")
    session_id = form_data.get("sessionId")
    phone_number = form_data.get("phoneNumber")
    service_code = form_data.get("serviceCode")

    user_input = text.strip().split("*")[-1] if text else ""
    response = ussd_menu.handle_request(
        session_id=session_id,
        user_input=user_input,
        phone_number=phone_number,
    )
    print(response, service_code, phone_number, session_id, user_input)
    return str(response)
