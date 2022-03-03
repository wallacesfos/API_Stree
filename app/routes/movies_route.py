from flask import Blueprint

from app.controllers.movies_controller import (
    get_series_by_genre,
    post_favorite,
    remove_favorite
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")

# bp_series.post("")(create_serie)
bp_movies.get("/<int:profile_id>")(get_series_by_genre)
bp_movies.post("/favorites")(post_favorite)
bp_movies.delete("/favorites")(remove_favorite)
