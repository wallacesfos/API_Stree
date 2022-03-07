from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.profile_model import ProfileModel
from flask import request, current_app, jsonify
from app import utils
from app.models.series_model import SeriesModel
from werkzeug.exceptions import NotFound


@jwt_required()
def create_profile():
    body = request.get_json()
    identity = get_jwt_identity()

    profiles = ProfileModel.query.filter_by(user_id=identity["id"]).all()

    try: 
        if len(body["name"]) < 4:
            raise IndexError()

        if len(profiles) >= 4:
            return {"error": "Maximum profiles reached"}, HTTPStatus.CONFLICT

        if not "kids" in body.keys():
            body["kids"] = False

        utils.analyze_keys(['name', "kids"], body)
        
        profile = ProfileModel(**body, user_id=identity['id'])
        profile.name = body['name'].title()

        current_app.db.session.add(profile)
        current_app.db.session.commit()

        return jsonify(profile), HTTPStatus.CREATED
        
    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST 
    except IndexError as error:
        return {'error': "Name must have 4 characters"}, HTTPStatus.BAD_REQUEST       
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST 


@jwt_required()
def get_profiles():
    identity = get_jwt_identity()
    profiles = ProfileModel.query.filter_by(user_id=identity["id"]).all()

    serializer = [
        {
            "id": profile.id,
            "name": profile.name,
            "kids": profile.kids
        } for profile in profiles
    ]

    return jsonify(serializer), HTTPStatus.OK


@jwt_required()
def update_profile(id):
    identity = get_jwt_identity()
    body = request.get_json()

    try: 
        profile = ProfileModel.query.filter_by(user_id=identity["id"], id=id).first_or_404("profile not found")

        profile.name = body['name']

        current_app.db.session.add(profile)
        current_app.db.session.commit()

        return {
            "id": profile.id,
            "name": profile.name,
            "user_id": profile.user_id
        }

    except KeyError:
        return {"error": "Must contain the keys: ['name']"}, HTTPStatus.BAD_REQUEST
    except NotFound as error:
        return {"error": error.description}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def delete_profile(id):
    identity = get_jwt_identity()

    try: 
        profile = ProfileModel.query.filter_by(user_id=identity["id"], id=id).first_or_404("profile not found")

        current_app.db.session.delete(profile)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except NotFound as error:
        return {"error": error.description}, HTTPStatus.NOT_FOUND
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST



@jwt_required()
def favorites_movies(id: int):
    try:
        profile = ProfileModel.query.filter_by(id=id).first_or_404("Profile not found")

    except NotFound as error:
        return {"error": error.description}, HTTPStatus.NOT_FOUND

    return jsonify(profile.movies), HTTPStatus.OK

@jwt_required()
def favorites_series(id: int):
    try:
        profile = ProfileModel.query.filter_by(id=id).first_or_404("Profile not found")

    except NotFound as error:
        return {"error": error.description}, HTTPStatus.NOT_FOUND

    return jsonify(profile.series), HTTPStatus.OK

