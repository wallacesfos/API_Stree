from flask import Flask
from app.routes.users_route import bp_users
from app.routes.profiles_routes import bp_profile
from app.routes.series_route import bp_series
from app.routes.episodes_route import bp_episodes
from app.routes.genders_routes import bp_genders
from app.routes.movies_routes import bp_movies


def init_app(app: Flask):
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_series)
    app.register_blueprint(bp_profile)
    app.register_blueprint(bp_episodes)
    app.register_blueprint(bp_genders)
    app.register_blueprint(bp_movies)
