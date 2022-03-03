from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from http import HTTPStatus
from app.utils import analyze_keys
from datetime import datetime as dt

from app.models.movies_model import MoviesModel


@jwt_required()
def get_most_seen_movies():
    movies = MoviesModel.query.all()
    list_view = [m.views for m in movies]

    quantity = 5 if len(movies) >= 5 else len(movies)
    most_seen = []

    for _ in range(quantity): 
        index = list_view.index(max(list_view))
        biggest_view = list_view.pop(index)
        movie = MoviesModel.query.filter_by(views=biggest_view).first()
        most_seen.append(movie)
    
    return jsonify(most_seen), 200

@jwt_required()
def get_most_recent_movies():
    movies = MoviesModel.query.all()
    released_date_list = [{
        'id': m.id,
        'diff_days': (dt.now() - m.released_date).days
        } for m in movies]
    
    released_date_list.sort(reverse=False, key=lambda arg: arg['diff_days'])
    quantity = 5 if len(movies) >= 5 else len(movies)

    most_recent = []
    for i in range(quantity): 
        id = released_date_list[i]['id']
        movie = MoviesModel.query.get(id)
        most_recent.append(movie)

    return jsonify(most_recent), 200



@jwt_required()
def create_movie():
    try:
        session = current_app.db.session
        data = request.get_json()
        keys = [
            "name",
            "image",
            "description",
            "subtitle",
            "dubbed",
            "views",
            "duration",
            "link",
            "classification",
            "released_date",
            "trailers"]
        
        administer = get_jwt_identity()
        if not administer["administer"]:
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