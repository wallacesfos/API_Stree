from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.models.user_model import UserModel
from app.exc import EmptyListError
from app.utils import find_by_genre



@jwt_required()
def post_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        serie = MoviesModel.query.filter_by(id=data["movie_id"]).first_or_404("Movie not found")
        profile.series.append(serie)
        current_app.db.session.add(profile)
        current_app.db.session.commit()

    except Exception as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify({}), HTTPStatus.NO_CONTENT