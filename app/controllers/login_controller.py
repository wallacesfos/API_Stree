from flask_jwt_extended import create_access_token
from app.models.user_model import UserModel
from flask import request
from app import utils


def login_user():
    body = request.get_json()
    
    try:
        utils.analyze_keys(["email", "password"], body)

        password = body.pop('password')

        found_user = UserModel.query.filter_by(email=body['email']).first()

        if not found_user or not found_user.verify_password(password):
            return {"message": "Password or email invalid"}, 400

        access_token = create_access_token(identity=found_user)

        return {"access_token": access_token}, 200
    except KeyError as e:
        return {"error": str(e)}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400