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
        
        if not valid_profile_kid():
            genre = GendersModel.query.filter(GendersModel.gender.ilike(f"{name}")).first()
        else:
            genre = GendersModel.query.filter(GendersModel.gender.ilike(f"{name}")).first()
            
        if video_type == "movies":
#TODO precisa pensar em um jeito de pegar genre.movies e verificar a classificação
            return jsonify(genre.movies), HTTPStatus.OK
        else:
#TODO precisa pensar em um jeito de pegar genre.series e verificar a classificação
            return jsonify(genre.series), HTTPStatus.OK
    
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
    
def valid_profile_kid():
    from app.models.profile_model import ProfileModel
    
    profile_id = request.get_json()["profile_id"]
    profile = ProfileModel.query.filter_by(id = profile_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), HTTPStatus.NOT_FOUND
    
    # if not profile in user.profiles:
    #     return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
    
    return profile.kids