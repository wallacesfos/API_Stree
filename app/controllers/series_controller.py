from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from sqlalchemy.orm import Query
from app.models.series_model import SeriesModel
from app.utils import analyze_keys
from app.exc import NaoEncontradosRegistrosError, PermissionError
from http import HTTPStatus

from app.models.series_model import SeriesModel
from app.models.user_model import UserModel
from app.models.profile_model import ProfileModel


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
    try:
        profile: ProfileModel = get_jwt_identity()
        classification = profile.kids

        title_name = request.args['title']
        genre_name = request.args['genre']

        if title_name and genre_name:
            series = find_by_genre(classification, genre_name, title_name) 
        elif title_name:
            if classification:
                series = SeriesModel.query.filter(SeriesModel.name.ilike(f"%{title_name}%"), SeriesModel.classification <= 16).all()
            else:
                series = SeriesModel.query.filter(SeriesModel.name.ilike(f"%{title_name}%")).all()
        elif genre_name:
            series = find_by_genre(classification, genre_name)
        else:
            if classification:
                series = SeriesModel.query.filter(SeriesModel.classification < 16).all()
            else:
                series = SeriesModel.query.all()
    
        if not series:
            raise NaoEncontradosRegistrosError(description="The database is empty.")

        return jsonify(series),200

    except NaoEncontradosRegistrosError as e:
        return {"error": e.description}, e.code
        

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
def delete_serie(id):
    try:
        session = current_app.db.session

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError

        serie = SeriesModel.query.filter_by(id=id).first()

        if not serie:
            return {"error": "Serie not found"}, 404

        episodes = serie.episodes
        
        for i in episodes:
            session.delete(i)
            session.commit()

        session.delete(serie)
        session.commit()

        return {}, 204

    except PermissionError:
        return {"error": "Admins only"},400


def find_by_genre(classification, genre_name, title_name = None):
    from app.models.series_genders_model import series_genders
    from app.models.gender_model import GendersModel

    genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{genre_name}%")).first().id
    
    if classification:
        series: Query = current_app.db.session.query(
            SeriesModel.id,
            SeriesModel.name,
            SeriesModel.image,
            SeriesModel.description,
            SeriesModel.seasons,
            SeriesModel.trailer,
            SeriesModel.created_at,
            SeriesModel.views,
            SeriesModel.dubbed,
            SeriesModel.subtitle,
            SeriesModel.classification,
            SeriesModel.released_date
    ).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(
    series_genders.gender_id == genre_id, SeriesModel.name.ilike(f"%{title_name}%"), SeriesModel.classification <= 16).all()
    else:
        series: Query = current_app.db.session.query(
            SeriesModel.id,
            SeriesModel.name,
            SeriesModel.image,
            SeriesModel.description,
            SeriesModel.seasons,
            SeriesModel.trailer,
            SeriesModel.created_at,
            SeriesModel.views,
            SeriesModel.dubbed,
            SeriesModel.subtitle,
            SeriesModel.classification,
            SeriesModel.released_date
        ).select_from(SeriesModel).join(series_genders).join(GendersModel).filter(
        series_genders.gender_id == genre_id, SeriesModel.name.ilike(f"%{title_name}%")).all()

    return [{
           "id": serie.id,
           "name": serie.name,
           "image": serie.image,
           "description": serie.description,
           "seasons": serie.seasons,
           "trailer": serie.trailer,
           "created_at": serie.created_at,
           "views": serie.views,
           "dubbed": serie.dubbed,
           "subtitle": serie.subtitle,
           "classification": serie.classification,
           "released_date": serie.released_date
        } for serie in series ]


   
  
    
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


