from flask import jsonify, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.exc import EmptyListError
from app.utils import find_by_genre


@jwt_required()
def get_movies_by_name(profile_id: int, title: str):
    try:
        movies = MoviesModel.query.filter_by(MoviesModel.name.ilike(f"%{title}%")).all()

        profile = ProfileModel.query.filter(id=profile_id).first()

        if not profile:
            return {"error": "Profile not found"}, HTTPStatus.NOT_FOUND

        if profile.kids:
            return jsonify([movie for movie in movies if movie.classification <= 13]), HTTPStatus.OK

        if not movies:
            raise EmptyListError

        return jsonify(movies), HTTPStatus.OK
    except EmptyListError as e:
        return {"error": e.description}, e.code
