from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify
from http import HTTPStatus

from app.utils import find_by_genre, analyze_keys
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


from datetime import datetime as dt
from app.exc import EmptyListError

from app.models.movies_model import MoviesModel
from app.models.profile_model import ProfileModel
from app.models.gender_model import GendersModel
from app.models.user_model import UserModel


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

    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return {"error": "This movie is already exists"}, HTTPStatus.CONFLICT


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
    try:
        movie: MoviesModel = MoviesModel.query.filter_by(id=id)
        data = request.get_json()

        keys = [
        "image",
        "description",
        "duration",
        "trailers",
        "link",
        "subtitle",
        "dubbed",
        "classification"]

        analyze_keys(keys, data, 'update')

        if not movie:
            return {"error": "Movie not found."}, HTTPStatus.NOT_FOUND
        
        movie.update(data, synchronize_session="fetch")
        current_app.db.session.commit()

    except PermissionError:
        return {"error": "Admins only"}, HTTPStatus.BAD_REQUEST

    except KeyError as e:
        return {"error": e.args[0]}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def get_most_seen_movies():
    movies_most_seen = MoviesModel.query.order_by(MoviesModel.views.desc()).limit(5).all()
   
    
    return jsonify(movies_most_seen), HTTPStatus.OK

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

    return jsonify(most_recent), HTTPStatus.OK


@jwt_required()
def get_appropriated_movie(profile_id: int):
    try:
        profile = ProfileModel.query.filter(id = profile_id).first()
        if not profile:
            return {"error": "Profile not found."}

        if profile.kids:
            movies = MoviesModel.query.filter(MoviesModel.classification <= 13).all()
            if not movies: raise EmptyListError(description="There is no appropriated movies to watch")
            return jsonify(movies), HTTPStatus.OK

        movies = MoviesModel.query.all()
        if not movies: raise EmptyListError(description="There is no movies to watch")

        return jsonify(movies), HTTPStatus.OK
    
    except EmptyListError as e:
        return {"Message": e.description}, e.code
      
@jwt_required()
def get_movies_by_name():
    movie_name = request.args.get("name")

    movies = MoviesModel.query.filter(MoviesModel.name.ilike(f"%{movie_name}%")).all()
    
    if not movies:
        return {"message": "Any movies were found"}, HTTPStatus.NOT_FOUND


    return jsonify(movies),HTTPStatus.OK

@jwt_required()
def add_to_gender():
    data = request.get_json()

    try:
        analyze_keys(["gender_id", "movie_id"], data)

        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            

        movie = MoviesModel.query.filter_by(id=data["movie_id"]).first_or_404("Movie not found")
        gender = GendersModel.query.filter_by(id=data["gender_id"]).first_or_404("Gender not found")
        movie.genders.append(gender)
        current_app.db.session.add(gender)
        current_app.db.session.commit()

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, 400
        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.NO_CONTENT

@jwt_required()
def remove_from_gender():
    data = request.get_json()
    try:
        analyze_keys(["gender_id", "movie_id"], data)
        
        administer = get_jwt_identity()

        if not administer["administer"]:
            raise PermissionError
            
        movie = MoviesModel.query.filter_by(id=data["movie_id"]).first_or_404("Movie not found")
        gender = GendersModel.query.filter_by(id=data["gender_id"]).first_or_404("Gender not found")
        remove = movie.genders.index(gender)
        movie.genders.pop(remove)
        current_app.db.session.add(movie)
        current_app.db.session.commit()
    
    except ValueError:
        return {"error": "film does not belong to the genre"}, HTTPStatus.BAD_REQUEST

    except NotFound as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND

    except KeyError as e:
        return {"error": e.args[0]}, 400
        
    except Exception:
        return {"error": "An unexpected error occurred"}, HTTPStatus.BAD_REQUEST
    
    return {}, HTTPStatus.OK

@jwt_required()
def post_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        movie = MoviesModel.query.filter_by(id=data["movie_id"]).first_or_404("movie not found")
        if movie in profile.movies:
            return jsonify({"error": "Is already favorite"}), HTTPStatus.CONFLICT
        
        profile.movies.append(movie)
        current_app.db.session.add(profile)
        current_app.db.session.commit()

    except Exception as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify({}), HTTPStatus.NO_CONTENT



@jwt_required()
def remove_favorite():
    try:
        data = request.get_json()
        user = UserModel.query.filter_by(id=get_jwt_identity()["id"]).first_or_404("User not found")
        profile = ProfileModel.query.filter_by(id=data["profile_id"]).first_or_404("Profile not found")
        
        if not profile in user.profiles:
            return jsonify({"error": "Invalid profile for user"}), HTTPStatus.CONFLICT
        
        movie = MoviesModel.query.filter_by(id=data["movie_id"]).first_or_404("movie not found")
        
        if not movie in profile.movies:
            return jsonify({"error": "movie not found in profile"}), HTTPStatus.NOT_FOUND
        
        remove = profile.movies.index(movie)
        profile.movies.pop(remove)
        current_app.db.session.add(profile)
        current_app.db.session.commit()
    
    except Exception as e:
        return {"error": e.description}, HTTPStatus.NOT_FOUND
    
    return jsonify({}), HTTPStatus.NO_CONTENT
  
@jwt_required()
def get_movie_by_id(id):    
    movie = MoviesModel.query.get(id)

    if not movie:
        return {"message": "Movie not found"}, HTTPStatus.NOT_FOUND

    movie.views += 1
    current_app.db.session.commit()
    
    return jsonify(movie), HTTPStatus.OK


@jwt_required()
def get_movies_by_genre(genre_name: str):

    movies = find_by_genre(genre_name, video_type="movies")

    return movies

