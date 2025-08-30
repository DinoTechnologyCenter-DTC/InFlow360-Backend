from pydantic import BaseModel, Field


class OTPRequestSchema(BaseModel):
    """OTP Request schema."""

    phone_number: str


class OTPResponseSchema(BaseModel):
    """OTP Response schema."""

    phone_number: str
    otp: str
