from wsgiref import headers
from . import env, randoms, env_secrets

def test_create_user_status_code(client, app):

    app.config["SQLALCHEMY_DATABASE_URI"] = env()    

    response = client.post("/users/register", json={
        "email": f"{randoms()}@hotmail.com",
        "password": "traquinagem123"
    })
    
    assert response.status_code == 201

def test_create_user_error_integrity_error_status_code(client, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = env()

    for i in range(2):
        response = client.post("/users/register", json={
            "email": "abacaxis@hotmail.com",
            "password": "traquinagem123"
        })

        if response.json == {'error': 'Email already exists'}:
            assert response.status_code == 409
    


def test_login_user_success_status_code(client, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = env()
    app.config["JWT_SECRET_KEY"] = env_secrets()

    random_test = randoms()

    client.post("/users/register", json={
        "email": f"{random_test}@hotmail.com",
        "password": "traquinagem123"
    })

    response = client.post('/users/login', json={
        "email": f"{random_test}@hotmail.com",
        "password": "traquinagem123"
    })

    assert response.status_code == 200
    

def test_login_user_error_account_invalid_json(client, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = env()
    app.config["JWT_SECRET_KEY"] = env_secrets()

    response = client.post('/users/login', json={
        "email": "birolinha123s93993uhhhhhhh@outlook.com.br.us",
        "password": "dajkdasjkjsadkasjdbasndkas"
    })

    assert response.json == {"message": "Password or email invalid"}



def test_update_user_error_missing_authorization(client, app):
    app.config["SQLALCHEMY_DATABASE_URI"] = env()
    app.config["JWT_SECRET_KEY"] = env_secrets()

    response = client.put('/users', json={
        "password": "dajkdasjkjsadkasjdbasndkas"
    })

    assert response.json == {'msg': 'Missing Authorization Header'}


def test_delete_users_error_missing_authorization(client,app):
    app.config["SQLALCHEMY_DATABASE_URI"] = env()
    app.config["JWT_SECRET_KEY"] = env_secrets()

    response = client.delete('/users')

    assert response.json == {'msg': 'Missing Authorization Header'}


