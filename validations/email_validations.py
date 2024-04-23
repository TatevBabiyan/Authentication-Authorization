import re
from fastapi import HTTPException


def validmail(mail):
    message = "The email must contain a valid format, such as name@example.com"
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, mail):
        return mail
    else:
        raise HTTPException(status_code=400, detail=f"Invalid E-Mail! {message}")
