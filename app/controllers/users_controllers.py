from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.exc import PermissionError
from app.models.user_model import UserModel
from flask import request, current_app
from sqlalchemy import exc
from datetime import timedelta
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
    
    except KeyError as error:
        return {'error': error.args[0]}, 400
    except exc.IntegrityError:
        return {"error": "Email already exists"}, 409
    except Exception:
        return {"error": "An unexpected error occurred"}, 400



def login_user():
    body = request.get_json()
    
    try:
        utils.analyze_keys(["email", "password"], body)

        password = body.pop('password')

        found_user = UserModel.query.filter_by(email=body['email']).first()


        if not found_user or not found_user.verify_password(password):
            return {"message": "Password or email invalid"}, 400

        access_token = create_access_token(identity=found_user, expires_delta=timedelta(hours=24))
        return {"access_token": access_token}, 200
    except KeyError as e:
        return {"error": e.args[0]}, 400
    except Exception:
        return {"error": "An unexpected error occurred"}, 400        



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
        return {"error": e.args[0]}, 400
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
        return {"error": e.args[0]}, 400
    except KeyError:
        return {"error": "Need to pass the ID"}, 400
    except exc.StatementError:
        return {"error": "id: integer, email: string, administer: Boolean"}
    except Exception:
        return {"error": "An unexpected error occurred"}, 400



