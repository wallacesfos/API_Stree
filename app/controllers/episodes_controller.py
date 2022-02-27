from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from app.models.episodes_model import EpisodesModel
from app.models.series_model import SeriesModel
from app.utils import analyze_keys
from app.exc import PermissionError


@jwt_required()
def get_episodes():
    episodes = EpisodesModel.query.all()
    
    if not episodes:
        return {"error": "No data found"},404

    return jsonify(episodes),200

@jwt_required()
def get_episode_by_serie_id(serie_id):
    serie = SeriesModel.query.filter_by(id=serie_id).first()
    episode = EpisodesModel.query.filter_by(id=serie_id).first()

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
    
    if not serie:
        return {"message": "Episode not found"}, 404

    return jsonify(episode_serialize),200