from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from app.models.gender_model import GendersModel

from app.utils import analyze_keys, find_by_genre, serializer
from app.exc import PermissionError, EmptyListError
from werkzeug.exceptions import NotFound
from http import HTTPStatus

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
    series = SeriesModel.query.all()

    if not series:
        return {"message": "Serie not found"}, HTTPStatus.NOT_FOUND

    serie_serializer = serializer(series)

    return jsonify(serie_serializer), HTTPStatus.OK


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
        "gender": serie.genders,
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
def get_serie_by_name():
    serie_name = request.args.get("name")
    serie_name = serie_name.title()
  
    serie = SeriesModel.query.filter_by(name=serie_name).first()
    
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
        "gender": serie.genders,
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
def get_serie_most_seen():
    series_most_seen = SeriesModel.query.order_by(SeriesModel.views.desc()).limit(5).all()
    
    serie_serializer = serializer(series_most_seen)
    
    return jsonify(serie_serializer), HTTPStatus.OK

@jwt_required()
def series_recents():
    series = SeriesModel.query.order_by(SeriesModel.created_at.desc()).all()
    
    serie_serializer = serializer(series)
    
    return jsonify(serie_serializer), HTTPStatus.OK

@jwt_required()
def get_appropriated_series(profile_id: int):
    try:
        profile = ProfileModel.query.filter_by(id = profile_id).first()
        if not profile:
            return {"error": "Profile not found."}

        if profile.kids:
            series = SeriesModel.query.filter(SeriesModel.classification <= 13).all()
            
            if not series: 
                raise EmptyListError(description="There is no appropriated series to watch")
            return jsonify(series), HTTPStatus.OK

        series = SeriesModel.query.all()
        if not series: 
            raise EmptyListError(description="There is no series to watch")

        return jsonify(series), HTTPStatus.OK
    
    except EmptyListError as e:
        return {"Message": e.description}, e.code

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
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
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
def add_to_gender():
    body = request.get_json()

    try:
        analyze_keys(["gender_id", "serie_id"], body)

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            

        serie = SeriesModel.query.filter_by(id=body["serie_id"]).first_or_404("Serie not found")
        gender = GendersModel.query.filter_by(id=body["gender_id"]).first_or_404("Gender not found")
        serie.genders.append(gender)
        current_app.db.session.add(gender)
        current_app.db.session.commit()

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, 400
        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def remove_from_gender():
    data = request.get_json()
    try:
        analyze_keys(["gender_id", "serie_id"], data)
        
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("serie not found")
        gender = GendersModel.query.filter_by(id=data["gender_id"]).first_or_404("Gender not found")
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
def get_series_by_genre(profile_id: int):
    try:
        profile = ProfileModel.query.filter_by(id = profile_id).first_or_404("Profile not found")

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


@jwt_required()
def add_to_gender():
    data = request.get_json()

    try:
        analyze_keys(["gender_id", "serie_id"], data)

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            

        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
        gender = GendersModel.query.filter_by(id=data["gender_id"]).first_or_404("Gender not found")
        serie.genders.append(gender)
        current_app.db.session.add(serie)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, 400
    
    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.UNAUTHORIZED



@jwt_required()
def remove_from_gender():
    data = request.get_json()
    try:
        analyze_keys(["gender_id", "serie_id"], data)
        
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            
        serie = SeriesModel.query.filter_by(id=data["serie_id"]).first_or_404("Serie not found")
        gender = GendersModel.query.filter_by(id=data["gender_id"]).first_or_404("Gender not found")
        serie.genders.pop(gender)
        current_app.db.session.add(serie)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT
    
    except ValueError:
        return {"error": "This serie does not belong to the genre"}, HTTPStatus.BAD_REQUEST

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
        
    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.UNAUTHORIZED
    

