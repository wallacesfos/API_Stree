import string
import random
from flask import current_app
from app.models.user_model import UserModel

def env():
      with open('./.env', 'r') as f:
        for linha in f:
            if 'SQLALCHEMY_DATABASE_URI' in linha:
                linhas = linha.split('=')
                return linhas[1].strip('\n')


def env_secrets():
      with open('./.env', 'r') as f:
        for linha in f:
            if 'JWT_SECRET_KEY' in linha:
                linhas = linha.split('=')
                return linhas[1].strip('\n')

def env_kids():
      with open('./.env', 'r') as f:
        for linha in f:
            if 'AGE_KIDS' in linha:
                linhas = linha.split('=')
                return linhas[1].strip('\n')


def randoms():
    length_of_string = 10
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

def turn_to_admim(email):
    user: UserModel = UserModel.query.filter_by(email=email).first()
    user.administer = True
    current_app.db.session.commit()