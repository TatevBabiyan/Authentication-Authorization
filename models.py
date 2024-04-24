import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String, unique=True, nullable=False)
    contact_info = Column(String(20), nullable=True)
    password = Column(String(60), nullable=False)
    is_verified = Column(String, nullable=True)


class TokenTable(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    access_token = Column(String, index=True)
    refresh_token = Column(String, index=True)
    status = Column(Boolean, default=True)
