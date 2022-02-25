from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from app.models.series_model import SeriesModel
from app.models.user_model import UserModel
from app.utils import analyze_keys
from app.exc import PermissionError

@jwt_required()
def create_serie():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = ["name", "image", "description", "seasons", "subtitle", "dubbed", "trailer"]
        
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
