from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.exc import PermissionError
from app.models.user_model import UserModel
from flask import request, current_app
from sqlalchemy import exc

from app import utils


@jwt_required()
def update_users():
    body = request.get_json()
    
    try:
        utils.analyze_keys(["password"], body)
        requests = get_jwt_identity()
        found_user = UserModel.query.filter_by(email=requests['email']).first()

        for key, value in body.items():
            found_user.password_to_hash = value

        current_app.db.session.add(found_user)
        current_app.db.session.commit()

        return {}, 204
    except KeyError as e:
        return {"error": str(e)}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400


@jwt_required()
def delete_user():
    user = get_jwt_identity()
    found_user = UserModel.query.filter_by(email=user['email']).first()
    current_app.db.session.delete(found_user)
    current_app.db.session.commit()

    return {}, 204


@jwt_required()
def update_users_admin():
    body = request.get_json()
    requests = get_jwt_identity()
    
    try:
        if requests['administer'] == False:
            raise PermissionError('Permission denied')

        found_user = UserModel.query.filter_by(id=body['id']).first()

        if not found_user:
            return {"message": "User not found"}, 404

        for key, value in body.items():
            if key == 'password':
                found_user.password_to_hash = value
            else:
                setattr(found_user, key, value)

        current_app.db.session.add(found_user)
        current_app.db.session.commit()
        
        return {
            "id": found_user.id,
            "email": found_user.email
        }
    
    except PermissionError as e:
        return {"error": str(e)}, 400
    except KeyError:
        return {"error": "Need to pass the ID"}, 400
    except exc.StatementError:
        return {"error": "id: integer, email: string, administer: Boolean"}
    except Exception:
        return {"error": "An unexpected error occurred"}, 400

