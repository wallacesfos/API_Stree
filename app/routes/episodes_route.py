from flask import Blueprint
from app.controllers.episodes_controller import create_episode
bp_episodes = Blueprint("episodes", __name__, url_prefix="/episodes")

bp_episodes.post("")(create_episode)


