from app.configs.database import db
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass

from app.models.user_model import UserModel
from app.models.series_model import SeriesModel
from app.models.favorite_series_model import favorite_series


@dataclass
class ProfileModel(db.Model):
    id: int
    name: str
    user_id: UserModel
    kids: bool

    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kids = Column(Boolean, default=False)
    
    user = relationship(UserModel, backref=backref('profiles'))
    series = relationship(SeriesModel, secondary=favorite_series, backref=backref('profiles'))
     