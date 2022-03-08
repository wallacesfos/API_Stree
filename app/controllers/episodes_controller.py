from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from werkzeug.exceptions import NotFound
from app.utils import analyze_keys
from app.exc import PermissionError
from http import HTTPStatus

from app.models.episodes_model import EpisodesModel
from app.models.series_model import SeriesModel
from sqlalchemy.exc import NoResultFound

@jwt_required()
def create_episode():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = ["season", "link", "series_id", "episode"]
        
        administer = get_jwt_identity()
        

        if not administer["administer"]:
            raise PermissionError

        analyze_keys(keys, data)

        episode = EpisodesModel(**data)

        session.add(episode)
        session.commit()

        return jsonify(episode), HTTPStatus.CREATED

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.UNAUTHORIZED

    except KeyError as e:
        return {"error": e.args[0]}

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def get_episodes():
    episodes = EpisodesModel.query.all()

    return jsonify(episodes), HTTPStatus.OK

@jwt_required()
def get_episode_by_id(id):
    try:
        episode = EpisodesModel.query.filter_by(id=id).one()

    except NoResultFound:
        return {"error": "Episode not found"}, HTTPStatus.NOT_FOUND
    
    return jsonify(episode), HTTPStatus.OK



@jwt_required()
def delete_episode(id):
    try:
        session = current_app.db.session
        administer = get_jwt_identity()
        
        if not administer["administer"]:
            raise PermissionError

        episode = EpisodesModel.query.filter_by(id=id).first()
        session.delete(episode)
        session.commit()

        return "", HTTPStatus.NO_CONTENT

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

   

