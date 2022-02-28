from flask import Blueprint
from app.models.profile_model import ProfileModel
from app.controllers.profiles_controller import create_profile, get_profiles, update_profile, delete_profile

bp_profile = Blueprint('profile', __name__, url_prefix="/profiles")

bp_profile.post('')(create_profile)
bp_profile.get('')(get_profiles)
bp_profile.patch('/<int:id>')(update_profile)
bp_profile.delete('/<int:id>')(delete_profile)