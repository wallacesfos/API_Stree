from flask import Blueprint
from app.controllers.episodes_controller import get_episodes, get_episode_by_serie_id

bp_episodes = Blueprint("episodes", __name__, url_prefix="/episodes")

bp_episodes.get("")(get_episodes)
bp_episodes.get("/<int:serie_id>")(get_episode_by_serie_id)
