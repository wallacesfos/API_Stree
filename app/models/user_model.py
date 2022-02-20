from app.configs.database import db
from sqlalchemy import Column, String, Boolean, Integer
from dataclasses import dataclass

@dataclass
class UserModel(db.Model):
    id: int
    email: str
    password: str
    administer: bool

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(130), nullable=False, unique=True)
    password = Column(String, nullable=False)
    administer = Column(Boolean, default=False)

