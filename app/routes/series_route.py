from flask import Blueprint
from app.controllers.series_controller import create_serie

bp_series = Blueprint("series", __name__, url_prefix="/series")

bp_series.post("")(create_serie)
