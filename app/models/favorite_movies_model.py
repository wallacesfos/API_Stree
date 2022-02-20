from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey


favorite_movies = db.Table('favorite_movies', 
    Column('id', Integer, primary_key=True), 
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('profile_id', Integer, ForeignKey('profiles.id'))
)