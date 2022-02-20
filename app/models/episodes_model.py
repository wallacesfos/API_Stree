from os import link
from app.configs.database import db
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass
from app.models.series_model import SeriesModel

@dataclass
class EpisodesModel(db.Model):
    id: int
    season: int
    link: str
    episode: int
    series_id: SeriesModel

    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    season = Column(Integer, nullable=False)
    link = Column(String, nullable=False)
    episode = Column(Integer, nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=False)

    serie = relationship(SeriesModel, backref='episodes')
    