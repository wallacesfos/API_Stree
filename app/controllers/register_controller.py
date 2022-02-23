from app.models.user_model import UserModel
from flask import request, current_app
from sqlalchemy import exc
from app import utils

def create_register():
    body = request.get_json()

    try:
        utils.analyze_keys(["email", "password"], body)

        password = body.pop("password")

        user = UserModel(**body)

        user.password_to_hash = password

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return {
            "msg": "user created successfully"
        }, 201
    
    except KeyError as e:
        return {'error': str(e)}, 400
    except exc.IntegrityError:
        return {"error": "Email already exists"}, 409
    except Exception:
        return {"error": "An unexpected error occurred"}, 400