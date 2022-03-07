from http import HTTPStatus
from flask import request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import analyze_keys
from app.models.gender_model import GendersModel
from app.exc import PermissionError
from sqlalchemy.exc import IntegrityError


@jwt_required()
def post_gender():
    try:
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
       
        body = request.get_json()
        keys = ["gender"]
        analyze_keys(keys, body)
        
        gender = GendersModel(**body)
        current_app.db.session.add(gender)
        current_app.db.session.commit()
        
        return jsonify(gender), HTTPStatus.CREATED

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST
    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"error": "gender already exists"}, HTTPStatus.CONFLICT
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def get_genders():
    
    gender = GendersModel.query.order_by(GendersModel.gender.asc()).all()
    
    return jsonify(gender), HTTPStatus.OK

@jwt_required()
def get_gender(id):
    
    gender = GendersModel.query.filter_by(id=id).first()
    
    if not gender:
        return {"error": "Gender not found"}, HTTPStatus.NOT_FOUND

    return jsonify(gender), HTTPStatus.OK

@jwt_required()
def delete_gender(id):
    try:

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
    
    
        gender = GendersModel.query.filter_by(id=id).first()
        if not gender:
            return {"msg": "Gender not found"}, HTTPStatus.NOT_FOUND
    
        gender.series = []
        gender.movies = []
        
        current_app.db.session.delete(gender)
        current_app.db.session.commit()

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def patch_gender(id): 
    try:
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
        
        body = request.get_json()
        keys = ["gender"]

        analyze_keys(keys, body)
        
        gender = GendersModel.query.filter_by(id=id).first()

        if not gender:
            return {"msg": "gender not found"}, HTTPStatus.NOT_FOUND
            
        gender.gender = body["gender"]
        
        current_app.db.session.add(gender)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    
    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST
    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"error": "gender already exists"}, HTTPStatus.CONFLICT
    