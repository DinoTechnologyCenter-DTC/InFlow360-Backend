"""Collection of validation functions."""

import phonenumbers


def phone_number_validator(phone_number: str) -> str:
    """Format and validate phone number."""
    try:
        try:
            _phone_number = phonenumbers.parse(phone_number, "TZ")
        except phonenumbers.phonenumberutil.NumberParseException:
            _phone_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.phonenumberutil.NumberParseException as error:
        msg = "Invalid phone number"
        raise ValueError(msg) from error

    if not phonenumbers.is_valid_number(_phone_number):
        msg = "Invalid phone number"
        raise ValueError(msg)
    return phonenumbers.format_number(
        _phone_number,
        phonenumbers.PhoneNumberFormat.E164,
    )
