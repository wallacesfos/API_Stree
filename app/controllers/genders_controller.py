from curses.ascii import HT
from http import HTTPStatus
from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import analyze_keys
from app.models.gender_model import GendersModel
from app.configs.database import db
from app.exc import PermissionError


@jwt_required()
def post_gender():
    admin = get_jwt_identity()["administer"]
    if not admin:
        # TODO não entrou no except PermissionError
        # raise PermissionError
        return {"error": "not admin"}, HTTPStatus.BAD_REQUEST
    
    try:
        #TODO permitiu salvar duplicado, mas a model está ok
        data = request.get_json()
        keys = ["gender"]
        analyze_keys(keys, data)
        
        gender = GendersModel(**data)
        current_app.db.session.add(gender)
        current_app.db.session.commit()
        
        return jsonify(gender), HTTPStatus.CREATED

    except PermissionError:
        return {"error": "not admin"}, HTTPStatus.BAD_REQUEST
    except KeyError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
