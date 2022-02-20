from app.configs.database import db
from sqlalchemy import Column, String, Integer
from dataclasses import dataclass


@dataclass
class SeriesModel(db.Model):
    id: int
    name: str
    image: str
    description: str
    seasons: int
    trailer: str

    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    seasons = Column(Integer, nullable=False)
    trailer = Column(String)
    
