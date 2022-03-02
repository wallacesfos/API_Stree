from turtle import update
from flask import Blueprint
from app.controllers.movies_controller import get_movies, create_movie, update_movie, delete_movie

bp_movies = Blueprint("movies", __name__, url_prefix="/movies")


bp_movies.get("")(get_movies)
bp_movies.post("")(create_movie)
bp_movies.patch("/<int:id>")(update_movie)
bp_movies.delete("/<int:id>")(delete_movie)