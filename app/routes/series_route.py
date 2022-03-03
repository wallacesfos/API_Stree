from flask import Blueprint

from app.controllers.series_controller import (
    create_serie,
    get_series,
    get_serie_by_id, 
    get_serie_by_name, 
    patch_serie_most_seen,
    series_recents, post_favorite,
    delete_serie,
    get_appropriated_series
    )

bp_series = Blueprint("series", __name__, url_prefix="/series")

bp_series.post("")(create_serie)
bp_series.get("")(get_series)
bp_series.get("/<int:id>")(get_serie_by_id)
bp_series.get("/<int:profile_id>")(get_appropriated_series)
bp_series.get("/recents")(series_recents)
bp_series.patch("/most_seen/<int:id>")(patch_serie_most_seen)
bp_series.get("/")(get_serie_by_name)
bp_series.post('/favorite')(post_favorite)
bp_series.delete("/<int:id>")(delete_serie)



