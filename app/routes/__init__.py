from flask import Flask
from app.routes.users_route import bp_users

from app.routes.series_route import bp_series

def init_app(app: Flask):
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_series)