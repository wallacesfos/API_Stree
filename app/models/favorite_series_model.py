from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


favorite_series = db.Table('favorite_series', 
    Column('id', Integer, primary_key=True), 
    Column('serie_id', Integer, ForeignKey('series.id')),
    Column('profile_id', Integer, ForeignKey('profiles.id'))
)