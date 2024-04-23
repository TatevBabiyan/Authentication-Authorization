from pydantic import BaseModel



class UserCreate(BaseModel):
    username: str
    email: str
    contact_info: str
    password: str


class RequestDetails(BaseModel):
    email: str
    password: str


class VerificationCreate(BaseModel):
    email: str
    is_verified: str



