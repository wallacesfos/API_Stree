from app.configs.database import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass
from app.models.user_model import UserModel


@dataclass
class ProfileModel(db.Model):
    id: int
    name: str
    user_id: UserModel

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship(UserModel, backref=backref('profiles'))

     