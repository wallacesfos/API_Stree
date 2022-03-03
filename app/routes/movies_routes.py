from flask import Blueprint
from app.controllers.movies_controller import get_most_seen_movies, create_movie, get_most_recent_movies

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.get("/most_seen")(get_most_seen_movies)
bp_movies.get("/most_recent")(get_most_recent_movies)
bp_movies.post("")(create_movie)