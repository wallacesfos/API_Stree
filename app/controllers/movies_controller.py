from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.exc import EmptyListError
from app.utils import find_by_genre


@jwt_required()
def update_movie(id: int):
    movie = MoviesModel.query.filter(id = id).one_or_404("Movie not found")
    
    movie.views += 1
    
    current_app.db.session.add(movie)
    current_app.db.session.commit()
    
    return {}, HTTPStatus.NO_CONTENT