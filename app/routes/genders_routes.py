from flask import Blueprint

from app.controllers.genders_controller import (
    get_gender, get_genders, post_gender
)

bp_genders = Blueprint("genders", __name__, url_prefix="/genders")

bp_genders.post('')(post_gender)
bp_genders.get('/<int:id>')(get_gender)
bp_genders.get('')(get_genders)