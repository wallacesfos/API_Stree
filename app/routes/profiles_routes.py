from flask import Blueprint
from app.models.profile_model import ProfileModel
from app.controllers.profiles_controller import create_profile, get_profiles

bp_profile = Blueprint('profile', __name__, url_prefix="/profiles")

bp_profile.post('')(create_profile)
bp_profile.get('')(get_profiles)