# main.py
import random
import string

from fastapi import FastAPI, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

import crud, models, schemas, utils
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db=db, user=user)
    return new_user



@app.post("/verify")
def verify_email(email: str, db: Session = Depends(get_db)):
    verified = crud.verify_user(email=email, db=db)
    return verified


@app.post("/login")
def login(request: schemas.RequestDetails, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=request.email)
    user2 = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not utils.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    if user2.is_verified is None:
        raise HTTPException(status_code=401, detail="User Not Verified")
    return {"message": "Login successful"}


@app.get("/getusers")
def get_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    return crud.get_all_users(skip=skip, limit=limit, db=db)
