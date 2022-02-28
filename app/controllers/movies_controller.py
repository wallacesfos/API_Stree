from operator import or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from sqlalchemy import or_
from app.models.movies_model import MoviesModel
from sqlalchemy.orm import Query

@jwt_required()
def get_movies_by_name(title):

    movies = MoviesModel.query.filter(or_(
        MoviesModel.name.ilike(f"%{title}%"),
        MoviesModel.description.ilike(f"%{title}"))
        ).all()

    if not movies:
        return {"error": "No data found"}, 404

    return jsonify(movies), 200


@jwt_required()
def get_movies_by_genre(genre_type):
    from app.models.movies_genders_model import movies_genders
    from app.models.gender_model import GendersModel

    genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{genre_type}%")).first().id

    movies: Query = current_app.db.session.query(
        MoviesModel.id,
        MoviesModel.name,
        MoviesModel.image,
        MoviesModel.description,
        MoviesModel.duration,
        MoviesModel.link,
        MoviesModel.trailers,
        MoviesModel.created_at,
        MoviesModel.views,
        MoviesModel.dubbed,
        MoviesModel.subtitle,
        MoviesModel.classification,
        MoviesModel.released_date
    ).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(
    movies_genders.gender_id == genre_id).all()


    return jsonify([
        {
           "id": movie.id,
           "name": movie.name,
           "image": movie.image,
           "description": movie.description,
           "duration": movie.duration,
           "link": movie.link,
           "trailers": movie.trailers,
           "created_at": movie.created_at,
           "views": movie.views,
           "dubbed": movie.dubbed,
           "subtitle": movie.subtitle,
           "classification": movie.classification,
           "released_date": movie.released_date
        } for movie in movies  ]), 200

