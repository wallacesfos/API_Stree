from http import HTTPStatus
from flask import jsonify, request

from app.models.movies_model import MoviesModel
from app.models.gender_model import GendersModel
from app.models.series_model import SeriesModel
from app.models.movies_genders_model import movies_genders
from app.models.series_genders_model import series_genders
from app.configs.database import db
from sqlalchemy import and_


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
        
        if video_type == "movies":
            if not valid_profile_kid():
                movies = db.session.query(MoviesModel).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(GendersModel.gender.ilike(f"%{name}%")).all()
                return jsonify(movies)
            else:
                movies = db.session.query(MoviesModel).select_from(MoviesModel).join(movies_genders).join(GendersModel).filter(and_(GendersModel.gender.ilike(f"%{name}%"), MoviesModel.classification <= 12)).all()
                return jsonify(movies)

        else:
            if not valid_profile_kid():
                series = db.session.query(SeriesModel).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(GendersModel.gender.ilike(f"%{name}%")).all()
                return jsonify(series)
            else:
                series = db.session.query(SeriesModel).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(and_(GendersModel.gender.ilike(f"%{name}%"), SeriesModel.classification <= 12)).all()
                return jsonify(series)
    
    except AttributeError:
        return {"Error": "Genre not found"}, HTTPStatus.NOT_FOUND



def serializer(series):
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
        


def check_values_from_profile(body):
    
    ...
    
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