import random
import string

from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from validations import email_validations, password_validation, name_validation, contact_validation
from utils import get_hashed_password

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    email_validations.validmail(user.email)
    password_validation.ValidPassword(user.password)
    contact_validation.valid_phone(user.contact_info)
    name_validation.validate_full_name(user.username)

    encrypted_password = get_hashed_password(user.password)

    db_user = models.User(username=user.username, email=user.email, contact_info=user.contact_info, password=encrypted_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def verify_user(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    user.is_verified = verification_code
    db.commit()

    return "User Verified"

