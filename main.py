import random
import string
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Header
from sqlalchemy.orm import Session

import crud
import models
import schemas
import utils
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


@app.post("/token")
async def login_for_access_token(request: schemas.RequestDetails, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=request.email)
    if not user or not utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        email = utils.verify_access_token(token, credentials_exception=HTTPException(status_code=401,
                                                                                     detail="Could not validate credentials"))
        return {"email": email}
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")


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
