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
            "id",
            "name",
            "image",
            "description",
            "subtitle",
            "dubbed",
            "views",
            "duration",
            "created_at",
            "updated_at",
            "link",
            "classification",
            "released_date",
            "trailers"]
        
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
        return {"error": e.args[0]}

    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST


