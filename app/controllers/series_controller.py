from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from itsdangerous import json
from sqlalchemy.orm import Query
from app.models.series_model import SeriesModel
from app.utils import analyze_keys
from app.exc import PermissionError

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

        return jsonify(serie), 201

    except PermissionError:
        return {"error": "Admins only"},400

    except KeyError as e:
        return {"error": str(e)}

    except Exception:
        return {"error": "An unexpected error occurred"}, 400


@jwt_required()
def get_series():
    series = SeriesModel.query.all()
    
    if not series:
        return {"error": "No data found"},404

    return jsonify(series),200

@jwt_required()
def get_serie_by_id(id):
    serie = SeriesModel.query.filter_by(id=id).first()

    if not serie:
        return {"message": "Serie not found"}, 404

    return jsonify(serie),200



@jwt_required()
def get_series_by_genre(genre_type):
    from app.models.series_genders_model import series_genders
    from app.models.gender_model import GendersModel

    genre_id = GendersModel.query.filter_by(GendersModel.gender.ilike(f"%{genre_type}%")).first().id

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
    series_genders.gender_id == genre_id).all()


    return jsonify([
        {
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
        } for serie in series  ]), 200