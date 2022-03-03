from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.models.user_model import UserModel
from app.exc import EmptyListError, PermissionError
from app.utils import find_by_genre


@jwt_required()
def delete_movie(id: int):
    try:
        if not get_jwt_identity()['administer']:
            raise PermissionError

        movie = MoviesModel.query.filter(id=id).one_or_404(discription="Movie not found")

        current_app.db.session.delete(movie)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT
    
    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

