import re
from fastapi import HTTPException


def valid_phone(phone_number):
    message = "The phone number must start with either:\n+374()... (including country code)\nor\n0()... (for local numbers)"
    pattern = r'^(?:\+374\d{8}|0\d{8,9})$'
    if re.match(pattern, phone_number):
        return phone_number
    else:
        return HTTPException(status_code=400, detail=f"Invalid Phone Number! {message}")
