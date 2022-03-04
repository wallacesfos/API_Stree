
def analyze_keys(keys, request):
    
    for key in request.keys():
        if not key in keys:
            raise KeyError(f"Must contain the keys: {keys}")

    try:
        for key in keys:
            request[key]
    except KeyError:
        raise KeyError(f"Must contain the keys: {keys}")

recorver_email_list = []

def find_by_genre(name: str):
    from app.models.gender_model import GendersModel
    
    try:
        genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{name}%")).first().id
        series = GendersModel.query.filter(id=genre_id).first().serie
        return series
    
    except AttributeError:
        return {"Error": "Genre not found"}, 404