import os
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr

load_dotenv()


class MailBody(BaseModel):
    subject: str
    recipient_email: EmailStr
    message: str
    body: str



HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD").replace(' ', '')
PORT = os.environ.get("MAIL_PORT", 587)
