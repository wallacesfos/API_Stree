from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from app import exc

from app.utils import analyze_keys, find_by_genre, valid_profile_kid, serializer
from app.exc import PermissionError, EmptyListError, InvalidProfileError, NotFoundError
from sqlalchemy import and_
from werkzeug.exceptions import NotFound

from app.models.series_model import SeriesModel
from app.models.user_model import UserModel
from app.models.profile_model import ProfileModel
from app.models.gender_model import GendersModel


@jwt_required()
def create_serie():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = ["name",
                 "image",
                 "description", 
                 "seasons", 
                 "subtitle", 
                 "dubbed", 
                 "trailer", 
                 "classification", 
                 "released_date"]
        
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
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def get_series():
    try:
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        if not valid_profile_kid(user):
            series = SeriesModel.query.all()
        else:
            series = SeriesModel.query.filter(SeriesModel.classification <= 13).all()
        if not series:
            return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND
            
        return jsonify(serializer(series)), HTTPStatus.OK
    
    except EmptyListError as e:
        return {"Message": e.description}, e.code

    except NotFoundError:
        return {"error": "Profile not found"}, HTTPStatus.NOT_FOUND
    
    except InvalidProfileError:
        return {"error": "Invalid profile for user"}, HTTPStatus.CONFLICT
        

@jwt_required()
def get_serie_by_id(id):
    user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
    if not valid_profile_kid(user):
        serie = SeriesModel.query.filter_by(id=id).first()
    else:
        serie = SeriesModel.query.filter(and_(SeriesModel.classification <= 12, SeriesModel.id == id)).first()


    if not serie:
        return {"message": "Serie not found or inappropriate"}, HTTPStatus.NOT_FOUND

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
        "gender": serie.genders,
        "episodes": [
            {
                "season": episode.season, 
                "link": episode.link, 
                "episode": episode.episode
            }for episode in serie.episodes
        ]
    }

    serie.views += 1
    current_app.db.session.commit()

    return jsonify(serie_serializer), HTTPStatus.OK


@jwt_required()
def get_serie_by_name(series_name: str):
    user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
    if not valid_profile_kid(user):
        series = SeriesModel.query.filter(SeriesModel.name.ilike(f"%{series_name}%")).all()
    else:
        series = SeriesModel.query.filter(and_(SeriesModel.classification <= 12, SeriesModel.name.ilike(f"%{series_name}%"))).all()
    
    if not series:
        return {"message": "Serie not found or inappropriate."}, HTTPStatus.NOT_FOUND

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
    }for serie in series]

    return jsonify(serie_serializer),HTTPStatus.OK


@jwt_required()
def get_serie_most_seen():
    user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
    if not valid_profile_kid(user):
        series = SeriesModel.query.order_by(SeriesModel.views.desc()).limit(5).all()
    else:
        series = SeriesModel.query.filter(SeriesModel.classification <= 12).order_by(SeriesModel.views.desc()).limit(5).all()
    
    
    return jsonify(serializer(series)), HTTPStatus.OK

@jwt_required()
def series_recents():
    user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
    if not valid_profile_kid(user):
        series = SeriesModel.query.order_by(SeriesModel.created_at.desc()).all()
    else:
        series = SeriesModel.query.filter(SeriesModel.classification <= 12).order_by(SeriesModel.created_at.desc()).all()
    
    
    return jsonify(serializer(series)), HTTPStatus.OK


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
        return {"error": "Admins only"}, HTTPStatus.UNAUTHORIZED
  
    
@jwt_required()
def post_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")

#TODO precisa levar esse código para valid_profile_kid, daqui:
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
#TODO até aqui

        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        if not valid_profile_kid(user):
            serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
        else:
            serie = SeriesModel.query.filter(and_(SeriesModel.id == data["serie_id"], SeriesModel.classification <= 12)).first_or_404("Serie not found or inappropriated")
        
        if serie in profile.series:
            return jsonify({"error": "Is already favorite"}), HTTPStatus.CONFLICT
        
        profile.series.append(serie)
        current_app.db.session.add(profile)
        current_app.db.session.commit()

    except Exception as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify({}), HTTPStatus.NO_CONTENT



@jwt_required()
def remove_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
        
        if not serie in profile.series:
            return jsonify({"error": "Serie not found in profile"}), HTTPStatus.NOT_FOUND
        
        remove = profile.series.index(serie)
        profile.series.pop(remove)
        current_app.db.session.add(profile)
        current_app.db.session.commit()
    
    except Exception as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify({}), HTTPStatus.NO_CONTENT

@jwt_required()
def add_to_genre():
    body = request.get_json()

    try:
        analyze_keys(["genre_id", "serie_id"], body)

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            

        serie = SeriesModel.query.filter_by(id=body["serie_id"]).first_or_404("Serie not found")
        gender = GendersModel.query.filter_by(id=body["genre_id"]).first_or_404("Gender not found")
        serie.genders.append(gender)
        current_app.db.session.add(gender)
        current_app.db.session.commit()

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def remove_from_genre():
    data = request.get_json()
    try:
        analyze_keys(["genre_id", "serie_id"], data)
        
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("serie not found")
        gender = GendersModel.query.filter_by(id=data["genre_id"]).first_or_404("Gender not found")
        remove = serie.genders.index(gender)
        serie.genders.pop(remove)
        current_app.db.session.add(serie)
        current_app.db.session.commit()
    
    except ValueError:
        return {"error": "film does not belong to the genre"}, HTTPStatus.BAD_REQUEST

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, 400
        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.OK



@jwt_required()
def get_series_by_genre(genre_name: str):

    series = find_by_genre(genre_name)

    return series


@jwt_required()
def update_serie(id: int):
    try:
        serie: SeriesModel = SeriesModel.query.filter_by(id=id)
        data = request.get_json()

        keys = [
        "image",
        "description", 
        "seasons", 
        "subtitle", 
        "dubbed", 
        "trailer", 
        "classification"]

        analyze_keys(keys, data, 'update')

        if not serie:
            return {"error": "Movie not found."}, HTTPStatus.NOT_FOUND
        
        serie.update(data, synchronize_session="fetch")
        current_app.db.session.commit()
     
    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.NO_CONTENT
    
