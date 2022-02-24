from flask import Blueprint
from app.controllers.users_controllers import update_users, delete_user, update_users_admin, create_register, login_user

bp_users = Blueprint("users", __name__, url_prefix="/users")

bp_users.put('')(update_users)
bp_users.delete('')(delete_user)
bp_users.put('/to_admin')(update_users_admin)
bp_users.post('/register')(create_register)
bp_users.post('/login')(login_user)