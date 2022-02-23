from flask import Flask
from app.routes.register_route import bp_register

def init_app(app: Flask):
    app.register_blueprint(bp_register)