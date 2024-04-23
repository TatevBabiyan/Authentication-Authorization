import re
from fastapi import HTTPException


def validate_full_name(name):
    message = "The Name must contain two or more alphabetical words separated by a space, where each word may include hyphens."
    pattern = r'^[a-zA-Z]+(?:-[a-zA-Z]+)*\s+[a-zA-Z]+(?:-[a-zA-Z]+)*$'
    if re.match(pattern, name):
        return name
    else:
        return HTTPException(status_code=400, detail=f"Invalid Name! {message}")
