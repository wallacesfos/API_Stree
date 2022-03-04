from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from werkzeug.security import generate_password_hash

from app.models.user_model import UserModel
from flask import request, current_app
from secrets import token_urlsafe
from sqlalchemy import exc
from datetime import timedelta
from flask_mail import Message
from os import getenv
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

        if found_user.verify_password(body["password"]):
            return {"error": "Password same as above"}, 409

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

def send_email_recovery():
    email = request.get_json()['email']
    email_hash = generate_password_hash(email)
    link = f"{request.base_url}/{email}?code={email_hash}"

    if not UserModel.query.filter_by(email=email).first():
        return {'error': 'email not found'}, 404

    msg = Message(
        subject = 'Recover Password',
        sender = getenv('MAIL_USERNAME'),
        recipients = [email],
        body = f'''
                Criação de senha temporária
            Click no link abaixo para a criação de uma senha temporária:
            {link}
        '''
    )

    utils.recorver_email_list.append(email_hash)
    current_app.mail.send(msg)
    return '', 200

def create_new_password(email):
    hash = request.args['code']

    if hash not in utils.recorver_email_list:
        return {'error': 'Resource not acessible'}, 404

    found_user: UserModel = UserModel.query.filter_by(email=email).first()
    
    new_password = token_urlsafe(8)
    found_user.password_to_hash = new_password

    current_app.db.session.add(found_user)
    current_app.db.session.commit()

    utils.recorver_email_list.pop(utils.recorver_email_list.index(hash))

    return {'msg': f'you temporary password is: {new_password}'}, 200
