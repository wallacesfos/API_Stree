from flask import Blueprint
from app.controllers.movies_controller import get_movies

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.get("")(get_movies)

