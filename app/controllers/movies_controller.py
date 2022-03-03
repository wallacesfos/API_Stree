from flask import jsonify, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.exc import EmptyListError
from app.utils import find_by_genre



@jwt_required()
def get_movies_by_genre(profile_id: int):
    try:
        profile = ProfileModel.query.filter(id = profile_id).first_or_404("Profile not found")

        request_genre = request.args.get('genre', None)
        if request_genre:
            movies = find_by_genre(request_genre, "movie")

        if profile.kids and request_genre:
            filtered_list = [movie for movie in movies if movie.classification <= 13]
            if not filtered_list: raise EmptyListError(description="There is no appropriated movies to watch")
            return jsonify(filtered_list), HTTPStatus.OK

        elif profile.kids:
            movies = MoviesModel.query.filter(MoviesModel.classification <= 13).all()
            if not movies: raise EmptyListError(description="There is no appropriated movies to watch")
            return jsonify(movies), HTTPStatus.OK
        
        elif request_genre:
            return jsonify(movies), HTTPStatus.OK

        else:
            movies = MoviesModel.query.all()
            if not movies: raise EmptyListError(description="There is no movies to watch")
            return jsonify(movies), HTTPStatus.OK
        
    except EmptyListError as e:
        return {"Message": e.description}, e.code


        