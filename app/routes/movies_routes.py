from flask import Blueprint
from app.controllers.movies_controller import get_movies_by_name, get_movies_by_genre

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.get("/<title>")(get_movies_by_name)
bp_movies.get("/<genre>")(get_serie_by_genre)

