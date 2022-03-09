from flask import Blueprint

from app.controllers.series_controller import (
    add_to_gender,
    create_serie,
    get_series,
    get_serie_by_id, 
    get_serie_by_name, 
    get_serie_most_seen, 
    series_recents, 
    post_favorite, 
    delete_serie,
    remove_favorite,
    get_series_by_genre,
    remove_from_gender,
    update_serie
)



bp_series = Blueprint("series", __name__, url_prefix="/series")

bp_series.post("")(create_serie)
bp_series.get("")(get_series)
bp_series.get("/<int:id>")(get_serie_by_id)
bp_series.get("/genre/<genre_name>")(get_series_by_genre)
bp_series.get("/profile/<int:profile_id>")(get_by_series)
bp_series.get("/recents")(series_recents)
bp_series.get("/most_seen")(get_serie_most_seen)
bp_series.get("/")(get_serie_by_name)
bp_series.post('/favorite')(post_favorite)
bp_series.delete("/<int:id>")(delete_serie)
bp_series.delete('/favorite')(remove_favorite)
bp_series.delete('/gender')(remove_from_gender)
bp_series.patch('/<int:id>')(update_serie)
bp_series.post('/gender')(add_to_gender)

