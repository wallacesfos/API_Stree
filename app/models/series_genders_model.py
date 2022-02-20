from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey




series_genders = db.Table('series_genders',
    Column('id', Integer, primary_key=True),
    Column('serie_id', Integer, ForeignKey('series.id')),
    Column('gender_id', Integer, ForeignKey('genders.id'))
)