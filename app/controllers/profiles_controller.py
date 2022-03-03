from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.profile_model import ProfileModel
from flask import request, current_app, jsonify
from app import utils


@jwt_required()
def create_profile():
    body = request.get_json()
    identity = get_jwt_identity()

    profiles = ProfileModel.query.filter_by(user_id=identity["id"]).all()

    try: 
        if len(profiles) >= 4:
            return {"error": "Maximum profiles reached"}, 400

        if not "kids" in body.keys():
            body["kids"] = False

        utils.analyze_keys(['name', "kids"], body)
        
        profile = ProfileModel(**body, user_id=identity['id'])
        profile.name = body['name'].title()

        current_app.db.session.add(profile)
        current_app.db.session.commit()

        return jsonify(profile), 201
        
    except KeyError as e:
        return {"error": e.args[0]}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400


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

    if serializer == []:
        return {"error": "Nada foi encontrado"}, 404

    return jsonify({"profile": serializer}), 200


@jwt_required()
def update_profile(id):
    identity = get_jwt_identity()
    body = request.get_json()

    try: 
        profiles = ProfileModel.query.filter_by(user_id=identity["id"]).all()

        for i in profiles:
            if id == i.id:
                profiles = 'True'

        if profiles != 'True':
            return {"error": "profile not found"}, 404

        profile = ProfileModel.query.filter_by(id=id).first()

        profile.name = body['name']

        current_app.db.session.add(profile)
        current_app.db.session.commit()

        return {
            "id": profile.id,
            "name": profile.name,
            "user_id": profile.user_id
        }
    except KeyError as e:
        return {"error": "Must contain the keys: 'name'"}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400

@jwt_required()
def delete_profile(id):
    identity = get_jwt_identity()

    try: 
        profiles = ProfileModel.query.filter_by(user_id=identity["id"]).all()

        for i in profiles:
            if id == i.id:
                profiles = 'True'

        if profiles != 'True':
            return {"error": "profile not found"}, 404

        profile = ProfileModel.query.filter_by(id=id).first()

        current_app.db.session.delete(profile)
        current_app.db.session.commit()

        return {},204
   
    except Exception:
        return {"error": "An unexpected error occurred"}, 400



@jwt_required()
def favorites_movies(id: int):

    profile = ProfileModel.query.filter(id=id).one_or_404("Profile not found")

    return jsonify(profile.movies), 200