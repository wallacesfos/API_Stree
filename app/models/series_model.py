from app.configs.database import db
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SeriesModel(db.Model):
    id: int
    name: str
    image: str
    description: str
    seasons: int
    trailer: str
    created_at: datetime
    views: int
    dubbed: bool
    subtitle: bool

    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    subtitle = Column(Boolean, nullable=False)
    dubbed = Column(Boolean, nullable=False)
    views = Column(Integer, default=0)
    seasons = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())   
    trailer = Column(String)
    
