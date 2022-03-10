from flask import Blueprint

from app.controllers.series_controller import (
    add_to_genre,
    create_serie,
    delete_serie,
    get_series,
    get_serie_by_id, 
    get_serie_by_name, 
    get_serie_most_seen, 
    get_series_by_genre,
    post_favorite, 
    remove_favorite,
    remove_from_genre,
    series_recents, 
    update_serie
)



bp_series = Blueprint("series", __name__, url_prefix="/series")

### series geral e por id
bp_series.post("")(create_serie)
bp_series.get("")(get_series)
bp_series.get("/<int:id>")(get_serie_by_id)
bp_series.patch('/<int:id>')(update_serie)
bp_series.delete("/<int:id>")(delete_serie)

### series e genre
bp_series.post('/genre')(add_to_genre)
bp_series.get("/genre")(get_series_by_genre)
bp_series.delete('/genre')(remove_from_genre)
### series e favorite
bp_series.post('/favorite')(post_favorite)
bp_series.delete('/favorite')(remove_favorite)
### series por filtros
bp_series.get("/recents")(series_recents)
bp_series.get("/most_seen")(get_serie_most_seen)
bp_series.get("/name")(get_serie_by_name)

