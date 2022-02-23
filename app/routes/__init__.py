from flask import Flask
from app.routes.register_route import bp_register
from app.routes.login_route import bp_login

def init_app(app: Flask):
    app.register_blueprint(bp_register)
    app.register_blueprint(bp_login)