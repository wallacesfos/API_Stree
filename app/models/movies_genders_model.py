from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


movies_genders = db.Table('movies_genders',
    Column('id', Integer, primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('gender_id', Integer, ForeignKey('genders.id'))
)