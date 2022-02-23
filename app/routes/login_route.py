from flask import Blueprint
from app.controllers.login_controller import login_user

bp_login = Blueprint('login', __name__, url_prefix='/login')

bp_login.post('')(login_user)