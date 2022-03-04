from flask import Blueprint

from app.controllers.movies_controller import (
    create_movie
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.post("")(create_movie)
