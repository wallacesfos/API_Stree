from flask import Blueprint

from app.controllers.movies_controller import (
    add_to_genre,
    create_movie,
    delete_movie,
    get_most_recent_movies,
    get_most_seen_movies,
    get_movies,
    get_movie_by_id,
    get_movies_by_genre,
    get_movies_by_name,
    post_favorite,
    remove_from_genre,
    update_movie,
)

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")

bp_movies.post("")(create_movie)
bp_movies.post('/genre')(add_to_genre)
bp_movies.post("/favorite")(post_favorite)

bp_movies.get("")(get_movies)
bp_movies.get("/<int:id>")(get_movie_by_id)
bp_movies.get('/genre/<genre_name>')(get_movies_by_genre)
bp_movies.get("/name/<name>")(get_movies_by_name)
bp_movies.get("/most_seen")(get_most_seen_movies)
bp_movies.get("/most_recent")(get_most_recent_movies)

bp_movies.patch("/<int:id>")(update_movie)

bp_movies.delete("/<int:id>")(delete_movie)
bp_movies.delete('/genre')(remove_from_genre)
