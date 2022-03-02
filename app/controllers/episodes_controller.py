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
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": str(e)}

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST

@jwt_required()
def get_episodes():
    episodes = EpisodesModel.query.all()
    
    if not episodes:
        return {"error": "No data found"}, HTTPStatus.NOT_FOUND

    return jsonify(episodes), HTTPStatus.OK

@jwt_required()
def get_episode_by_serie_id(serie_id):
    try:
        serie = SeriesModel.query.filter_by(id=serie_id).first()
        episode = EpisodesModel.query.filter_by(id=serie_id).first()

        if not serie:
            return {"message": "Episode not found"}, HTTPStatus.NOT_FOUND

        episode_serialize = {
            
            "series_id": episode.series_id,
            "name": serie.name,
            "image": serie.image,
            "description": serie.description,
            "subtitle": serie.subtitle,
            "dubled": serie.dubbed,
            "episodes":[
                {
                    "season": episode.season, 
                    "link": episode.link, 
                    "series_id": episode.series_id,
                    "episode": episode.episode
                }
            ]
        }
        return jsonify(episode_serialize), HTTPStatus.OK
    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND


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

   

def get_episode_by_id(id):
    try:
        episode = EpisodesModel.query.filter_by(id=id).one()
    except NoResultFound:
        return {"msg": "Episode not found"}, HTTPStatus.NOT_FOUND
    
    return jsonify(episode), HTTPStatus.OK

