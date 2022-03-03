from flask import jsonify, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.exc import EmptyListError
from app.utils import find_by_genre


@jwt_required()
def get_movies_by_name(profile_id: int, title: str):

    movies = MoviesModel.query.filter_by(MoviesModel.name.ilike(f"%{title}%")).all()

    profile = ProfileModel.query.filter(id=profile_id).one_or_404("Profile not found")
    if profile.kids:
        return jsonify([movie for movie in movies if movie.classification <= 13]), HTTPStatus.OK

    return jsonify(movies), HTTPStatus.OK