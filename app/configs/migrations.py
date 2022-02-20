from flask import Flask
from flask_migrate import Migrate

from app.models import series_genders_model


def init_app(app: Flask):
    Migrate(app, app.db)

    from app.models import episodes_model, favorite_movies_model, favorite_series_model, gender_model, movies_genders_model, movies_model, profile_model, series_genders_model, series_model, user_model