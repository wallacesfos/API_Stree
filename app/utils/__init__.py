from http import HTTPStatus
from flask import jsonify, request


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

    from app.models.gender_model import GendersModel
    
    try:
        genre_id = GendersModel.query.filter(GendersModel.gender.ilike(f"{name}")).first()
        
        if video_type == "movies":
#TODO precisamos pensar em um jeito de pegar genre.movies e verificar a classificação
            return jsonify(genre_id.movies), HTTPStatus.OK
        else:
#TODO precisamos pensar em um jeito de pegar genre.series e verificar a classificação
            return jsonify(genre_id.series), HTTPStatus.OK
    
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