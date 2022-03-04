from flask import Blueprint

from app.controllers.movies_controller import (
    post_favorite,
    remove_favorite,
    get_movies_by_name
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")

# bp_series.post("")(create_serie)
bp_movies.post("/favorites")(post_favorite)
bp_movies.delete("/favorites")(remove_favorite)
bp_movies.get("/<int:profile_id>/<title>")(get_movies_by_name)

