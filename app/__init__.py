from flask import Flask
from app.configs import database, migrations, jwt
from app import routes
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    database.init_app(app)
    migrations.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app