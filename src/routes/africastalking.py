"""Africas talkning Routes."""

from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, Response, status

from src.models.tables import Session, get_session
from src.schemas.auth import OTPRequestSchema, OTPResponseSchema
from src.services.africastalking.sms import africastalking_sms
from src.services.africastalking.ussd import ussd_menu
from src.services.auth import create_access_token

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
    # service_code = form_data.get("serviceCode")

    user_input = text.strip().split("*")[-1] if text else ""
    response = ussd_menu.handle_request(
        session_id=session_id,
        user_input=user_input,
        phone_number=phone_number,
    )

    return Response(str(response), media_type="text/plain")


@router.post("/otp")
async def send_otp(
    data: OTPRequestSchema,
    session: Annotated[Session, Depends(get_session)],
) -> dict:
    """Send OTP."""
    phone_number = data.phone_number
    otp = "123456"  # Generate OTP here

    africastalking_sms.send_sms(phone_number, f"Your OTP is {otp}")

    return {"status": "success", "data": {"phone_number": phone_number}}


@router.post("/verify-otp")
async def verify_otp(
    data: OTPResponseSchema,
    session: Annotated[Session, Depends(get_session)],
) -> dict:
    """Verify OTP."""
    phone_number = data.phone_number
    otp = data.otp
    if otp == "123456":  # Replace with actual OTP verification logic
        jwt = create_access_token(user_id=str(uuid4()))
        return Response(
            content={"token": {"value": jwt, "type": "Bearer"}},
            status_code=status.HTTP_200_OK,
        )
    return Response(
        content={"status": "error", "message": "Invalid OTP"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
