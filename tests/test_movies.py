from app.models.movies_model import MoviesModel
from app.models.profile_model import ProfileModel
from app.models.user_model import UserModel
from tests import env, env_secrets, env_kids, randoms, turn_to_admim 

def test_post_movie_whithout_token(client, app):

    app.config['SQLALCHEMY_DATABASE_URI'] = env()

    request = client.post('/movies', json={
	"name":"senhor dos aneis",
	"image":"xx",
	"description":"xxxxxx",
	"subtitle": True,
	"dubbed": True,
	"duration": 2,
	"link":"yy",
	"classification":18,
	"released_date":"05/07/1998",
	"trailers":"aaaa"
    })

    assert request.status_code == 401


def test_post_movies_not_been_admim(client, app):
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
        '/movies', 
        headers={"authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )

    assert request.status_code == 400


def test_post_movies_by_admim(client, app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )
    assert request.status_code == 201

def test_post_movie_missing_keys(client, app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "trailers":"ddddd"}
    )

    assert request.status_code == 400



def test_get_movie_by_id(client,app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )
    
    
    client.post(
        '/profiles',
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name": random_name, "kids":False}
    )

    profile_id = ProfileModel.query.filter_by(user_id=user.id).first()
    movie: MoviesModel = MoviesModel.query.filter_by(name=random_name.title()).first()
  
    request = client.get(
        f'/movies/{movie.id}', 
        headers={"Authorization": f"Bearer {token}"},
        json={"profile_id": profile_id.id} 
    )

    assert request.status_code == 200


def test_get_unregistered_movie_by_id_(client,app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )
    
    
    client.post(
        '/profiles',
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name": random_name, "kids":False}
    )

    profile_id = ProfileModel.query.filter_by(user_id=user.id).first()
    movie: MoviesModel = MoviesModel.query.filter_by(name=random_name.title()).first()
    
    request = client.get(
        f'/movies/600000000000000464664646446465416516565', 
        headers={"Authorization": f"Bearer {token}"},
        json={"profile_id": profile_id.id} 
    )

    assert request.status_code == 404



def test_patch_movie(client,app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )

    new_description = randoms()

    movie: MoviesModel = MoviesModel.query.filter_by(name=random_name.title()).first()
    request = client.patch(
        f'/movies/{movie.id}', 
        headers={"Authorization": f"Bearer {token}"},
        json={"description":new_description} 
    )

    assert request.status_code == 204


def test_delete_movie(client, app):
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
        '/movies', 
        headers={"Authorization": f"Bearer {token}"}, 
        json={"name":random_name,
            "image":"xx",
            "description":"xxxxxx",
            "subtitle": True,
            "dubbed": True,
            "duration": 1,
            "link":"xx",
            "classification":10,
            "released_date":"05/07/2019",
            "trailers":"ddddd"}
    )

    movie: MoviesModel = MoviesModel.query.filter_by(name=random_name.title()).first()
    request = client.delete(
        f'/movies/{movie.id}', 
        headers={"Authorization": f"Bearer {token}"} 
        )

    assert request.status_code == 204 