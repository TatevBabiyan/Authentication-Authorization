import datetime
import random
import string

from jose import jwt

from models import User,TokenTable
from fastapi import FastAPI, Depends, HTTPException,status
from utils import create_access_token, create_refresh_token, verify_password, get_password_hash, JWT_SECRET_KEY, \
    ALGORITHM
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session
from auth_bearer import JWTBearer
import crud
import models
import schemas
from config import MailBody
from database import SessionLocal, engine
from mailer import send_mail

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/login', response_model=schemas.TokenSchema)
def login(request: schemas.RequestDetails, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    token_db = models.TokenTable(user_id=user.id, access_token=access_token, refresh_token=refresh_token, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }



@app.get('/getusers')
def getusers(session: Session = Depends(get_db)):
    user = session.query(models.User).all()
    return user


@app.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = get_password_hash(request.new_password)
    user.password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}



@app.post("/register")
def register_user(user: schemas.UserCreate, tasks: BackgroundTasks, db: Session = Depends(get_db)):
    new_user = crud.create_user(db=db, user=user)
    verification_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    subject = "Verify Your Email Address"
    message = f"Your verification code is: {verification_code}."
    mail_body = MailBody(subject=subject, recipient_email=user.email, message=message, body=message)
    tasks.add_task(send_mail, mail_body.dict())
    return new_user


@app.post("/verify")
def verify_email(user: schemas.VerificationCreate, db: Session = Depends(get_db)):
    verified = crud.verify_user(user=user, db=db)
    return verified


@app.get("/getusers")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_users(skip=skip, limit=limit, db=db)

