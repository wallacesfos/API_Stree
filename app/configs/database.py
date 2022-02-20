from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app: Flask):
    db.init_app(app)
    app.db = db
    from app.models import episodes_model, favorite_movies_model, favorite_series_model, gender_model, movies_genders_model, movies_model, profile_model, series_genders_model, series_model, user_model