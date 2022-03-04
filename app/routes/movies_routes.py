from flask import Blueprint

from app.controllers.movies_controller import (
    create_movie,
    delete_movie,
    update_movie,
    get_most_recent_movies,
    get_most_seen_movies
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")

bp_movies.get("/most_seen")(get_most_seen_movies)
bp_movies.get("/most_recent")(get_most_recent_movies)
bp_movies.post("")(create_movie)
bp_movies.delete("/<int:id>")(delete_movie)
bp_movies.patch("/<int:id>")(update_movie)

