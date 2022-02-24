from flask import Blueprint

bp_users = Blueprint("users", __name__, url_prefix="/users")

bp_users.post('')()