from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify

from app.utils import analyze_keys, find_by_genre
from app.exc import PermissionError, EmptyListError
from http import HTTPStatus

from app.models.series_model import SeriesModel
from app.models.user_model import UserModel
from app.models.profile_model import ProfileModel

from app.configs.database import db





@jwt_required()
def create_serie():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = ["name", "image", "description", "seasons", "subtitle", "dubbed", "trailer", "classification", "released_date"]
        
        administer = get_jwt_identity()
        

        if not administer["administer"]:
            raise PermissionError

        analyze_keys(keys, data)
        data["name"] = data["name"].title()

        serie = SeriesModel(**data)

        session.add(serie)
        session.commit()

        return jsonify(serie), HTTPStatus.CREATED

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": e.args[0]}

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def get_series():
    series = SeriesModel.query.all()
    
    if not series:
        return {"error": "No data found"}, HTTPStatus.NOT_FOUND

    return jsonify(series),HTTPStatus.OK


@jwt_required()
def get_serie_by_id(id):
    serie = SeriesModel.query.filter_by(id=id).first()

    if not serie:
        return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND

    serie_serializer = {
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
        "episodes": [
            {
                "season": episode.season, 
                "link": episode.link, 
                "episode": episode.episode
            }for episode in serie.episodes
        ]
    }

    return jsonify(serie_serializer), HTTPStatus.OK


@jwt_required()
def patch_serie_most_seen(id):
    serie = SeriesModel.query.get(id)
    
    if not serie:
        return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND
    
    serie.views += 1
    
    current_app.db.session.add(serie)
    current_app.db.session.commit()

    
    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def get_serie_by_name():
    serie_name = request.args.get("name")
    serie_name = serie_name.title()
    new_str = ""

    for i in serie_name:
        if i == "%":
            new_str += " "
        else:
            new_str += i
            
    
    serie = SeriesModel.query.filter_by(name=new_str).first()
    
    if not serie:
        return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND

    serie_serializer = {
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
        "episodes": [
            {
                "season": episode.season, 
                "link": episode.link, 
                "episode": episode.episode
            }for episode in serie.episodes
        ]
    }

    return jsonify(serie_serializer),HTTPStatus.OK

@jwt_required()
def delete_serie(id):

    try:

        session = current_app.db.session

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError

        serie = SeriesModel.query.filter_by(id=id).first()

        if not serie:
            return {"error": "Serie not found"}, HTTPStatus.NOT_FOUND

        episodes = serie.episodes
        
        for i in episodes:

            session.delete(i)
            session.commit()

        session.delete(serie)
        session.commit()

        return {}, 204

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST
  
    
@jwt_required()
def series_recents():
    series = SeriesModel.query.order_by(SeriesModel.created_at.desc()).all()
    
    return jsonify(series), HTTPStatus.OK

    
@jwt_required()
def post_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
        profile.series.append(serie)
        current_app.db.session.add(profile)
        current_app.db.session.commit()

    except Exception as e:
        return {"error": e.description}, HTTPStatus.BAD_REQUEST
    
    return jsonify({}), HTTPStatus.NO_CONTENT



@jwt_required()
def get_series_by_genre(profile_id: int):
    try:
        profile = ProfileModel.query.filter(id = profile_id).first_or_404("Profile not found")

        request_genre = request.args.get('genre', None)
        if request_genre:
            series = find_by_genre(request_genre)

        if profile.kids and request_genre:
            filtered_list = [serie for serie in series if serie.classification <= 13]
            if not filtered_list: raise EmptyListError(description="There is no appropriated series to watch")
            return jsonify(filtered_list), HTTPStatus.OK

        elif profile.kids:
            series = SeriesModel.query.filter(SeriesModel.classification <= 13).all()
            if not series: raise EmptyListError(description="There is no appropriated series to watch")
            return jsonify(series), HTTPStatus.OK
        
        elif request_genre:
            return jsonify(series), HTTPStatus.OK

        else:
            series = SeriesModel.query.all()
            if not series: raise EmptyListError(description="There is no series to watch")
            return jsonify(series), HTTPStatus.OK
        
    except EmptyListError as e:
        return {"Message": e.description}, e.code