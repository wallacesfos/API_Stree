from flask import Blueprint

from app.controllers.movies_controller import (
    update_movie
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.patch("/<int:id>")(update_movie)

