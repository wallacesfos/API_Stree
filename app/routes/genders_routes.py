from flask import Blueprint

from app.controllers.genders_controller import delete_gender, get_gender, patch_gender, post_gender, get_genders

bp_genders = Blueprint("genders", __name__, url_prefix="/genders")

bp_genders.post('')(post_gender)
bp_genders.get('/<int:id>')(get_gender)
bp_genders.get('')(get_genders)
bp_genders.delete('/<int:id>')(delete_gender)
bp_genders.patch('<int:id>')(patch_gender)
