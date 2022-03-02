from flask import Blueprint
from app.controllers.episodes_controller import create_episode, get_episodes, get_episode_by_serie_id, get_episode_by_id

bp_episodes = Blueprint("episodes", __name__, url_prefix="/episodes")

bp_episodes.post("")(create_episode)
bp_episodes.get("")(get_episodes)
bp_episodes.get("/by_serie/<int:serie_id>")(get_episode_by_serie_id)
bp_episodes.get("/<int:id>")(get_episode_by_id)