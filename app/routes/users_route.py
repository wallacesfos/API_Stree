from flask import Blueprint
from app.utils import recovery_hash
from app.controllers.users_controllers import create_new_password, update_users, delete_user, create_register, login_user, send_email_recovery

bp_users = Blueprint("users", __name__, url_prefix="/users")

bp_users.put('')(update_users)
bp_users.delete('')(delete_user)
bp_users.post('/register')(create_register)
bp_users.post('/login')(login_user)
bp_users.post('/forgot_password')(send_email_recovery)
bp_users.get(f'/forgot_password/{recovery_hash}')(create_new_password)