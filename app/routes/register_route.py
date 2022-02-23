from flask import Blueprint
from app.controllers.register_controller import create_register

bp_register = Blueprint('register', __name__, url_prefix='/register')

bp_register.post('')(create_register)