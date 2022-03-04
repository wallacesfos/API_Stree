from app.configs.database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass
from app.models.movies_model import MoviesModel
from app.models.series_model import SeriesModel
from app.models.movies_genders_model import movies_genders
from app.models.series_genders_model import series_genders


@dataclass
class GendersModel(db.Model):
    id: int
    gender: str
    
    __tablename__ = 'genders'

    id = Column(Integer, primary_key=True)
    gender = Column(String, nullable=False, unique=True)
    
    movies = relationship(MoviesModel, secondary=movies_genders, backref=backref('genders'))
    series = relationship(SeriesModel, secondary=series_genders, backref=backref('genders'))