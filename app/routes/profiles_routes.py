from flask import Blueprint
from app.models.profile_model import ProfileModel
from app.controllers.profiles_controller import (
    create_profile, 
    favorites_movies, 
    get_profiles, 
    update_profile, 
    delete_profile,
    favorites_movies
    favorites_series
)

bp_profile = Blueprint('profile', __name__, url_prefix="/profiles")

bp_profile.post('')(create_profile)
bp_profile.get('')(get_profiles)
bp_profile.patch('/<int:id>')(update_profile)
bp_profile.delete('/<int:id>')(delete_profile)
bp_profile.get('/<int:id>/movies')(favorites_movies)
bp_profile.get('/<int:id>/series')(favorites_series)
