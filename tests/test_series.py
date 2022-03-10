from app.models.series_model import SeriesModel 
from app.models.profile_model import ProfileModel
from app.models.user_model import UserModel
from tests import env, env_secrets, env_kids, randoms, turn_to_admim 

def test_post_serie_whithout_token(client, app):

    app.config['SQLALCHEMY_DATABASE_URI'] = env()

    request = client.post('/series', json={
	"name":"Neo genesis evangelion",
	"image":"xx",
	"description":"xxxxxx",
    "seasons": 2,
	"subtitle": True,
	"dubbed": True,
	"classification":14,
	"released_date":"05/07/1991",
	"trailer":"aaaa"
    })

    assert request.status_code == 401


def test_post_serie_not_been_admim(client, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()

    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    token = signin.json["access_token"]
    
    request = client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
        "image":"xx",
        "description":"xxxxxx",
        "seasons": 2,
        "subtitle": True,
        "dubbed": True,
        "classification":14,
        "released_date":"05/07/1991",
        "trailer":"aaaa"}
    )

    assert request.status_code == 400


def test_post_serie_by_admim(client, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)

    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    token = signin.json['access_token']

    request = client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx",
        "seasons": 2,
	    "subtitle": True,
	    "dubbed": True,
	    "classification":14,
	    "released_date":"05/07/1991",
	    "trailer":"aaaa"}
    )
    assert request.status_code == 201

def test_post_serie_missing_keys(client, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)

    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    token = signin.json['access_token']

    request = client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx"}
    )

    assert request.status_code == 400



def test_get_serie_by_id(client,app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)
    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    user:UserModel = UserModel.query.filter_by(email=email).first()
    token = signin.json['access_token']

    client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx",
        "seasons": 2,
	    "subtitle": True,
	    "dubbed": True,
	    "classification":14,
	    "released_date":"05/07/1991",
	    "trailer":"aaaa"}
    )
    
    
    client.post(
        '/profiles',
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name": random_name, "kids":False}
    )

    profile_id = ProfileModel.query.filter_by(user_id=user.id).first()
    serie: SeriesModel = SeriesModel.query.filter_by(name=random_name.title()).first()
  
    request = client.get(
        f'/series/{serie.id}', 
        headers={"Authorization": f"Bearer {token}"},
        json={"profile_id": profile_id.id} 
    )

    assert request.status_code == 200


def test_get_unregistered_serie_by_id_(client,app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)
    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    user:UserModel = UserModel.query.filter_by(email=email).first()
    token = signin.json['access_token']

    client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx",
        "seasons": 2,
	    "subtitle": True,
	    "dubbed": True,
	    "classification":14,
	    "released_date":"05/07/1991",
	    "trailer":"aaaa"}
    )
    
    
    client.post(
        '/profiles',
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name": random_name, "kids":False}
    )

    profile_id = ProfileModel.query.filter_by(user_id=user.id).first()
    serie: SeriesModel = SeriesModel.query.filter_by(name=random_name.title()).first()
    
    request = client.get(
        f'/serie/600000000000000464664646446465416516565', 
        headers={"Authorization": f"Bearer {token}"},
        json={"profile_id": profile_id.id} 
    )

    assert request.status_code == 404



def test_patch_serie(client,app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)
    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    token = signin.json['access_token']
    
    client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx",
        "seasons": 2,
	    "subtitle": True,
	    "dubbed": True,
	    "classification":14,
	    "released_date":"05/07/1991",
	    "trailer":"aaaa"}
    )

    new_description = randoms()

    serie: SeriesModel = SeriesModel.query.filter_by(name=random_name.title()).first()
    request = client.patch(
        f'/series/{serie.id}', 
        headers={"Authorization": f"Bearer {token}"},
        json={"description":new_description} 
    )

    assert request.status_code == 204


def test_delete_serie(client, app):
    app.config['SQLALCHEMY_DATABASE_URI'] = env()
    app.config['JWT_SECRET_KEY'] = env_secrets()

    email = f'{randoms()}@gmail.com'
    random_name = randoms()
    
    client.post("/users/register", json={
        "email": email,
        "password": "traquinagem123"
    })

    turn_to_admim(email)

    signin = client.post("/users/login", json={
        "email": email,
        "password": "traquinagem123"
    })

    token = signin.json['access_token']
    
    client.post(
    '/series',
    headers={"Authorization": f"Bearer {token}"},  
    json={"name":random_name,
	    "image":"xx",
	    "description":"xxxxxx",
        "seasons": 2,
	    "subtitle": True,
	    "dubbed": True,
	    "classification":14,
	    "released_date":"05/07/1991",
	    "trailer":"aaaa"}
    )

    serie: SeriesModel = SeriesModel.query.filter_by(name=random_name.title()).first()
    request = client.delete(
        f'/series/{serie.id}', 
        headers={"Authorization": f"Bearer {token}"} 
        )

    assert request.status_code == 204 