from flask import Blueprint
from app.controllers.series_controller import create_serie, get_series, get_serie_by_id, get_serie_by_name, post_serie_most_seen

bp_series = Blueprint("series", __name__, url_prefix="/series")

bp_series.post("")(create_serie)
bp_series.get("")(get_series)
bp_series.get("/<int:id>")(get_serie_by_id)
bp_series.post("/most_seen/<int:id>")(post_serie_most_seen)
bp_series.get("/nome_da_serie")(get_serie_by_name)

