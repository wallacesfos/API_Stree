from operator import or_
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from sqlalchemy import or_
from app.models.movies_model import MoviesModel

@jwt_required()
def get_movies_by_name(title):

    movies = MoviesModel.query.filter(or_(
        MoviesModel.name.ilike(f"%{title}%"),
        MoviesModel.description.ilike(f"%{title}"))
        ).all()

    if not movies:
        return {"error": "No data found"}, 404

    return jsonify(movies), 200


@jwt_required()
def get_movies_by_genre(genre):
    ...


