from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from werkzeug.exceptions import NotFound
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
    try:
        serie = SeriesModel.query.filter_by(id=serie_id).first_or_404(description="Serie id not found!")
        episode = EpisodesModel.query.filter_by(id=serie_id).first_or_404(description="Serie id not found!")

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

        return jsonify(episode_serialize),200

    except NotFound as e:
        return {"error": e.description}, 404
