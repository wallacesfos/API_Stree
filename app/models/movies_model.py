from app.configs.database import db
from sqlalchemy import Column, String, Integer
from dataclasses import dataclass
from sqlalchemy.orm import relationship, backref
from app.models.profile_model import ProfileModel
from app.models.favorite_movies_model import favorite_movies

@dataclass
class MoviesModel(db.Model):
    id: int
    name: str
    image: str
    description: str
    duration: int
    link: str
    trailers: str

    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    link = Column(String, nullable=False)
    trailers = Column(String)

    profile = relationship(ProfileModel, secondary=favorite_movies, backref=backref('movies'))

    