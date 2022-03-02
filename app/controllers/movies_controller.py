from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from sqlalchemy.orm import Query
from app.utils import analyze_keys
from app.exc import NaoEncontradosRegistrosError, PermissionError
from http import HTTPStatus

from app.models.movies_model import MoviesModel
from app.models.user_model import UserModel
from app.models.profile_model import ProfileModel










@jwt_required()
def get_movies():
    try:
        title_name = request.args['title']
        genre_name = request.args['genre']

        if title_name and genre_name:
            movies = find_by_genre(genre_name, title_name) 
        elif title_name:
            movies = MoviesModel.query.filter(MoviesModel.name.ilike(f"%{title_name}%")).all()
        elif genre_name:
            movies = find_by_genre(genre_name)
        else:
            movies = MoviesModel.query.all()
    
        if not movies:
            raise NaoEncontradosRegistrosError(description="The database is empty.")

        return jsonify(movies),200

    except NaoEncontradosRegistrosError as e:
        return {"error": e.description}, e.code



def find_by_genre(genre_name, title_name = None):
    from app.models.movies_genders_model import movies_genders
    from app.models.gender_model import GendersModel

    genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{genre_name}%")).first().id

    movies: Query = current_app.db.session.query(
            MoviesModel.id,
            MoviesModel.name,
            MoviesModel.image,
            MoviesModel.description,
            MoviesModel.subtitle,
            MoviesModel.dubbed,
            MoviesModel.views,
            MoviesModel.duration,
            MoviesModel.created_at,
            MoviesModel.updated_at,
            MoviesModel.link,
            MoviesModel.classification,
            MoviesModel.released_date,
            MoviesModel.trailers
        ).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(
        movies_genders.gender_id == genre_id, MoviesModel.name.ilike(f"%{title_name}%")).all()

    return [{
        "id" : movies.id,
        "name" : movies.name,
        "image" : movies.image,
        "description" : movies.description,
        "subtitle" : movies.subtitle,
        "dubbed" : movies.dubbed,
        "views" : movies.views,
        "duration" : movies.duration,
        "created_at" : movies.created_at,
        "updated_at" : movies.updated_at,
        "link" : movies.link,
        "classification" : movies.classification,
        "released_date" : movies.released_date,
        "trailers" : movies.trailers
        } for movies in movies  ]

