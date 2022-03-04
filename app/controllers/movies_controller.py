from flask import jsonify, request,current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from app.models.profile_model import ProfileModel
from app.models.movies_model import MoviesModel
from app.exc import EmptyListError
from app.utils import find_by_genre, analyze_keys


@jwt_required()
def create_movie():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = [
            "name",
            "image",
            "description",
            "duration",
            "trailers",
            "link",
            "subtitle",
            "dubbed",
            "classification",
            "released_date"]
        
        if not get_jwt_identity()["administer"]:
            raise PermissionError

        analyze_keys(keys, data)
        data["name"] = data["name"].title()

        movie = MoviesModel(**data)

        session.add(movie)
        session.commit()

        return jsonify(movie), HTTPStatus.CREATED

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_movie(id: int):
    try:
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError

        movie = MoviesModel.query.filter_by(id=id).first()

        if not movie:
            return {"message": "Movie not found"}, HTTPStatus.NOT_FOUND

        current_app.db.session.delete(movie)
        current_app.db.session.commit()

        return {}, HTTPStatus.NO_CONTENT

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_movie(id: int):
    movie = MoviesModel.query.filter_by(id=id).first()

    if not movie:
        return {"error": "Movie not found."}, HTTPStatus.NOT_FOUND
    
    movie.views += 1
    
    current_app.db.session.add(movie)
    current_app.db.session.commit()
    
    return {}, HTTPStatus.NO_CONTENT
