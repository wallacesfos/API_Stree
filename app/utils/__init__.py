
recorver_email_list = []

def analyze_keys(keys, request):
    
    for key in request.keys():
        if not key in keys:
            raise KeyError(f"Must contain the keys: {keys}")

    try:
        for key in keys:
            request[key]
    except KeyError:
        raise KeyError(f"Must contain the keys: {keys}")



def find_by_genre(name: str, video_type: str = "series"):

    from app.models.gender_model import GendersModel
    
    try:
        genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{name}%")).first()
        print(genre_id)
        if video_type == "movies":
            return GendersModel.query.filter(id=genre_id).first().movie
        else:
            return GendersModel.query.filter(id=genre_id).first().serie
    
    except AttributeError:
        return {"Error": "Genre not found"}, 404

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
    
