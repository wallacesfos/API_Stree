from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import UserModel
from flask import request, current_app
from app import utils


@jwt_required()
def update_users():
    body = request.get_json()
    
    try:
        utils.analyze_keys(["password"])
        requests = get_jwt_identity()
        found_user = UserModel.query.filter_by(email=requests['email']).first()

        for key, value in body.items():
            found_user.password = value

        current_app.db.session.add(found_user)
        current_app.db.session.commit()

        return {}, 204
    except KeyError as e:
        return {"error": str(e)}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400