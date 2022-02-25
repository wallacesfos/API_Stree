from flask import Blueprint
from app.controllers.series_controller import get_serie_by_id

bp_series = Blueprint("bp_series", __name__, url_prefix="/series")

bp_series.get("/<int:id>")(get_serie_by_id)