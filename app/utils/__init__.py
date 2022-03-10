from http import HTTPStatus
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.configs.database import db
from app.models.user_model import UserModel
from app.models.gender_model import GendersModel
from app.models.series_model import SeriesModel
from app.models.series_genders_model import series_genders
from app.models.movies_model import MoviesModel
from app.models.movies_genders_model import movies_genders


recorver_email_list = []

def analyze_keys(keys, request, type=None):
    
    for key in request.keys():
        if not key in keys:
            raise KeyError(f"Must contain the keys: {keys}")

    if not type:
        try:
            for key in keys:
                request[key]
        except KeyError:
            raise KeyError(f"Must contain the keys: {keys}")



def find_by_genre(name: str, video_type: str = "series"):

    
    try:
        user = get_jwt_identity()
        user_model = UserModel.query.filter(UserModel.email.ilike(user['email']) ).first()
        
        if video_type == "movies":
            if not valid_profile_kid():
                movies = db.session.query(MoviesModel).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(GendersModel.gender.ilike(f"%{name}%")).all()
                return jsonify(movies)
            else:
                movies = db.session.query(MoviesModel).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(and_(GendersModel.gender.ilike(f"%{name}%"), MoviesModel.classification <= 12)).all()
                return jsonify(movies)

        else:
            if not valid_profile_kid(user_model):
                series = db.session.query(SeriesModel).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(GendersModel.gender.ilike(f"%{name}%")).all()
                return jsonify(series)
            else:
                series = db.session.query(SeriesModel).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(and_(GendersModel.gender.ilike(f"%{name}%"), SeriesModel.classification <= 12)).all()
                return jsonify(series)
    
    except AttributeError:
        return {"Error": "Genre not found"}, HTTPStatus.NOT_FOUND

def serializer_movies(movies):
    return [{
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
        "released_date": movie.released_date,
        "gender": movie.genders,
    } for movie in movies]
    
def serializer_movie(movie):
    return {
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
        "released_date": movie.released_date,
        "gender": movie.genders,
    }

def serializer_series(series):
    serie_serializer = [{
        "id": serie.id,
        "name": serie.name,
        "description": serie.description,
        "image": serie.image,
        "seasons": serie.seasons,
        "trailer": serie.trailer,
        "created_at": serie.created_at,
        "views": serie.views,
        "dubbed": serie.dubbed,
        "subtitle": serie.subtitle,
        "classification": serie.classification,
        "released_date": serie.released_date,
        "gender": serie.genders,
        "episodes": [
            {
                "season": episode.season, 
                "link": episode.link, 
                "episode": episode.episode
            }for episode in serie.episodes
        ]
        } for serie in series]
    return serie_serializer

def serializer_serie(serie):
    return {
        "id": serie.id,
        "name": serie.name,
        "description": serie.description,
        "image": serie.image,
        "seasons": serie.seasons,
        "trailer": serie.trailer,
        "created_at": serie.created_at,
        "views": serie.views,
        "dubbed": serie.dubbed,
        "subtitle": serie.subtitle,
        "classification": serie.classification,
        "released_date": serie.released_date,
        "gender": serie.genders,
        "episodes": [
            {
                "season": episode.season, 
                "link": episode.link, 
                "episode": episode.episode
            }for episode in serie.episodes
        ]
        }


    
def valid_profile_kid(user):
    from app.models.profile_model import ProfileModel
    from app.exc import InvalidProfileError, NotFoundError
    
    profile_id = request.get_json()["profile_id"]
    profile = ProfileModel.query.filter_by(id = profile_id).first()
        
    if not profile:
        raise NotFoundError()
    
    if not profile in user.profiles:
        raise InvalidProfileError()
        
    return profile.kids