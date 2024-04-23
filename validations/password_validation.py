import re
from fastapi import HTTPException


def ValidPassword(password):
    message = "The Password must contain at least 8 characters, including one letter, one digit, and may include special characters @$!%*?&"
    regex = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$'
    if re.fullmatch(regex, password):
        return password
    else:
        raise HTTPException(status_code=400, detail=f"Invalid Password! {message}")
