from flask_jwt_extended import jwt_required
from flask import current_app, jsonify
from sqlalchemy.orm.exc import NoResultFound

from app.models.series_model import SeriesModel

def get_serie_by_id(id):
    serie = SeriesModel.query.filter_by(id=id).first()

    if not serie:
        return {"message": "Serie not found"}, 404

    return jsonify(serie),200