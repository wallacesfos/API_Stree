import string
import random

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


def randoms():
    length_of_string = 10
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string))