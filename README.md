# Api - Stree

## Overview:

O **Stree** é uma plataforma de streaming de filmes e séries da atualidade ao alcance de um clique!

Com seu cadastro poderá acessar às melhores obras do audiovisual dubladas e legendas. Poderá navegar por gêneros e aproveitar do melhor estilo que te agrada.

Pensado para a família, o **Stree** tem o controle de materiais adequados para seus filhos curtirem sem preocupação.

## **Orientações**:

- Todas as requisições get estarão submetidas à um perfil associado à um usuário;
- As requisições do perfil entregam conteúdos de acordo com a sua classificação kids;
- Todas as requisições de obras deverão ser autenticadas;
- Caso não tenha nenhum conteúdo na rota de requisição genérica não será estourado um erro, será retornada uma lista vazia;
- A rota de criar usuário é pública. Qualquer um pode criar um usuário;
- A rota de criar perfil é privada. Um único usuário pode criar até 4 perfis;
- O usuário só poderá acessar os conteúdos sob um perfil definido;
- Um perfil pode ter infinitas obras favoritas entre séries e filmes;
- Um usuário só poderá se tornar um usuário administrador por alteração direta do desenvolvedor no banco de dados;

- Usuários não administradores poderão:
    - criar perfis;
    - alterar nome e estado de kids do perfil;
    - deletar um perfil;
    - adicionar, sob um id de um perfil, series e filmes aos favoritos;
    - remover, sob um id de um perfil, series e filmes dos favoritos;
    - acessar todas as obras filmes e séries;
    - acessar obras filtradas por nome;
    - acessar obras filtradas por gênero;
    - acessar obras filtradas por mais vistos;
    - acessar obras filtradas por mais recentes adicionadas ao catálogo;
    - acessar obras filtradas por favoritos de um perfil;
    - acessar episódios de uma determinada série;
    - acessar obra, filme ou série, por ID;
    
- Usuários administradores poderão:
    - usuários administradores poderão;
    - todas as funções do não administradores;
    - adicionar filmes e séries ao catálogo;
    - alterar informações de um filme ou série;
    - remover filmes e séries do catálogo;
    - adicionar gênero à lista de gêneros;
    - remover gênero da lista de gêneros;
    - associar um gênero à um filme ou série;
    - desassociar um gênero de um filme ou série;
    - adicionar episódio à uma série;
    - deletar episódio de uma série

## RESUMO DAS ROTAS

**USERS**
POST - /users/register Registra um usuário
POST - /users/login Efetua login
PATCH - /users Altera a senha do usuário
DELETE - /users Delete o usuário
POST - /users/forgot_password Envia email para usuário, com link para mudar a senha, não precisa estar logado

**PROFILE ROUTES**

POST - /profiles   Cria um novo perfil para o usuário logado

GET - /profiles   Retorna todos os perfis do usuário logado. O máximo de perfis é 4.

GET - /profiles/movies/<int:id>   Retorna a lista de filmes favoritados pelo usuário. O id é referente ao id do perfil.

GET - /profiles/series/<int:id>    Retorna a lista de séries favoritadas pelo usuário. O id é referente ao id do perfil.

PATCH - /profiles/<int:id>   Altera o nome do perfil já criado. O id é referente ao id do perfil.

DELETE - /profiles/<int:id>   Exclui um perfil associado ao usuário logado. O id é referente ao id do perfil.

**SERIES ROUTES**
POST - /series Inclui uma série
POST - /series/genre Adiciona uma série à um gênero
POST - /series/favorite Adiciona uma série aos favoritos de um perfil

GET - /series Todos as séries
GET - /series/name/name?name=name_to_search Todos as séries que tenham determinada palvra
GET - /series/genre/genre?genre=genre Todos as séries de um determinado gênero
GET - /series/most_seen As 5 primeiras séries mais assistidos
GET - /series/most_recent Em até 5 séries em ordem decrescente de lançamento
GET - /series/<int:id> Um série referente ao id descrito

PATCH - /series/<int:id> Atualiza informações da série de id indicado

DELETE - /series/<int:id> Deleta a série do id indicado
DELETE - /series/gender Remove uma série de um gênero
DELETE - /series/favorite Remove uma série dos favoritos de um perfil

**EPISODES ROUTES**

POST ****- /episodes     Adiciona um episódio à uma série

GET - /episodes Retorna todos os episódios do banco de dados

GET ****- /episodes/<int:id>  Retorna um episódio específico pelo id

DELETE **-** /epiosdes/<int:id> Remove um episódio do banco de dados

**MOVIES ROUTES**
POST - /movies/genre Adiciona um filme à um gênero
POST - /movies/favorite Adiciona um filme aos favoritos de um perfil

GET - /movies Todos os filmes
GET - /movies/name/name?name=name_to_search Todos os filmes que tenham determinada palavra
GET - /movies/genre/genre?genre=genre Todos os filmes de um determinado gênero
GET - /movies/most_seen Os 5 primeiros filmes mais assistidos
GET - /movies/most_recent Em até 5 filmes em ordem decrescente de lançamento
GET - /movies/<int:id> Um filme referente ao id descrito

PATCH - /movies/<int:id> Atualiza informações do filme de id indicado

DELETE - /movies/<int:id> Deleta o filme de id indicado
DELETE - /movies/genrer Remove um filme de um gênero
DELETE - /movies/favorite Remove um filme dos favoritos de um perfil

**GENDERS ROUTES**

POST - /genders Adiciona um gênero

GET - /genders Retorna todos os gêneros registrados

GET - /genders/<int:id> Retorna um gênero

DELETE - /genders/int:id   Remove do banco de dados um gênero existente

PATCH - /genders/int:id   Altera o nome de um gênero já criado

- **USERS**
    - **POST** /users/register
        - Rota não protegida
        - Corpo da requisição
        
        ```json
        
        {
        	"email": "johnvlogs@gmail.com",
        	"password": "traquinas123",
        }
        ```
        
        - Retorno da requisição status code 201 (CREATED)
        
        ```json
        **{
         "msg": "user created successfully"
        }, 201**
        
        ```
        
        - Retorno da requisição caso o email já exista, status code 409 (CONFLICT)
        
        ```json
        **{
         "error": "email já existe"
        }, 409**
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['email', 'password']"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos tenham o tamanho menor que 6, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Email and Password must have 6 characters"
        }
        ```
        
    - **POST /**users/login
        - Rota não protegida
        - Corpo da requisição
        
        ```json
        
        {
        		"email": "johnvlogs@gmail.com",
        		"password": "traquinas123"
        }
        ```
        
        - Retorno da requisição, status code 201 (CREATED)
        
        ```json
        **{**
         "id": 1,
         **"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }**
        ```
        
        - Retorno da requisição caso dos dados(VALORES) estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"message": "Password or email invalid"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos(KEYS) estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['email', 'password']"
        }
        ```
        
    - **PATCH** /users
        - Rota protegida
        - Formato da requisição:
        
        ```json
        {
        	"password": "dadadada"
        }
        ```
        
        - Retorno da rota, status code 204 (NO_CONTENT)
        
        ```json
        {}
        ```
        
        - Caso a senha seja a mesma que a anterior, status code 409 (CONFLICT)
        
        ```jsx
        {"error": "Password same as above"}
        ```
        
        - Retorno da requisição caso alguns dos campos(KEYS) estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['password']"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos tenham o tamanho menor que 6, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Email and Password must have 6 characters"
        }
        ```
        
    - **DELETE** /users
        - Rota protegida
        - Não passará nada na requisição
        - Retorno da rota, status code 204 (NO_CONTENT)
        
        ```json
        {}
        ```
        
    - **POST** /users/forgot_password
        - Rota não protegida
        - Corpo da requisição
        
        ```json
        
        {
        	"email": "johnvlogs@gmail.com",
        }
        ```
        
        - Retorno da rota, status code 204 (NO_CONTENT)
        
        ```json
        {}
        ```
        
        - Retorno da requisição caso alguns dos campos(KEYS) estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['password']"
        }
        ```
        
        - Retorno da requisição caso email não exista, status code 404(NOT_FOUND)
        
        ```json
        {
        	"error": "email not found"
        }
        ```
        

- **PROFILES**
    - **POST** /profiles
        - Rota deve ser privada
        - Corpo da requisição
        
        ```json
        {
        	"name": "Nome do Perfil 1",
        	"kids": false
        }
        ```
        
        - Retorno da requisição , 201 (CREATED)
        
        ```json
        
        {
        	"id": 12,
        	"name": "Nome Do Perfil 2",
        	"user_id": 3,
        	"kids": false
        }, 201
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400(BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['name', 'kids']"
        }
        ```
        
        - Retorno da requisição caso tente criar mais que 4 perfis , status code 409 (CONFLICT)
        
        ```json
        {
        "error": "Maximum profiles reached"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos tenham o tamanho menor que 6, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Name must have 4 characters"
        }
        ```
        
    - **GET** /profiles
        - Rota deve ser privada
        - Deve retornar apenas profiles do usuário logado
        - Corpo da requisição
        
        ```json
        {}
        ```
        
        - Retorno da requisição 200 (OK)
        
        ```json
        {
        	[
        	{
        		"id": 1,
        		"name": "Nome Do Perfil 1",
        		"kids": false
        	},
        	{
        		"id": 2,
        		"name": "Nome Do Perfil 2",
        		"kids": false
        	},
        	{
        		"id": 3,
        		"name": "Nome Do Perfil 2",
        		"kids": false
        	},
        	{
        		"id": 4,
        		"name": "Nome Do Perfil 2",
        		"kids": false
        	}
        ]}, 200
        ```
        
        - Retorno da requisição caso não tenha perfil criado. 200 (OK)
        
        ```json
        {
        	[]
        }, 200
        ```
        
    - **PATCH** /profiles/<int:id>
        - Rota deve ser privada
        - Corpo da requisição
        
        ```json
        {
        	"name": "Novo nome do perfil 1"
        }
        ```
        
        - Retorno da requisição 200 (OK)
        
        ```json
        {
        	"id": 15,
        	"name": "Novo nome do perfil 15",
        	"user_id": 3
        }, 200
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['name']"
        }
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "profile not found"
        }
        ```
        
    - **DELETE**  /profiles/<int:id>
        - Rota deve ser privada
        - Corpo da requisição
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Profile not found"
        }
        ```
        
    - **FAVORITES**
        - **FAVORITE_MOVIES** GET/profiles/movies/<profile_id>
            - Retorno da requisição caso não tenha filmes criado. 200 (OK)
            
            ```json
            {
            	[]
            }, 200
            ```
            
            - Retorno da requisição caso não tenha movies criado. 200 (OK)
            
            ```json
            {
            	[
            		{
            			"id": 10,
            			"name": "Naruto05",
            			"image": "www.google.com.png",
            			"description": "naruto um garoto com a raposa",
            			"seasons": 20,
            			"trailer": "gogle.com.br",
            			"created_at": "Wed, 02 Mar 2022 18:04:34 GMT",
            			"views": 0,
            			"dubbed": false,
            			"subtitle": true,
            			"classification": 18,
            			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
            		},
            		{
            			"id": 6,
            			"name": "Naruto03",
            			"image": "www.google.com.png",
            			"description": "naruto um garoto com a raposa",
            			"seasons": 20,
            			"trailer": "gogle.com.br",
            			"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
            			"views": 5,
            			"dubbed": false,
            			"subtitle": true,
            			"classification": 18,
            			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
            		}
            	]
            }, 200
            
            ```
            
        - **FAVORITE_SERIES** GET/profile/series/<id>
            - Retorno da requisição caso não tenha series criado. 200 (OK)
            
            ```json
            {
            	[]
            }, 200
            ```
            
            - Retorno da requisição caso não tenha series criado. 200 (OK)
            
            ```json
            {
            	[
            		{
            			"id": 10,
            			"name": "Naruto05",
            			"image": "www.google.com.png",
            			"description": "naruto um garoto com a raposa",
            			"seasons": 20,
            			"trailer": "gogle.com.br",
            			"created_at": "Wed, 02 Mar 2022 18:04:34 GMT",
            			"views": 0,
            			"dubbed": false,
            			"subtitle": true,
            			"classification": 18,
            			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
            		},
            		{
            			"id": 6,
            			"name": "Naruto03",
            			"image": "www.google.com.png",
            			"description": "naruto um garoto com a raposa",
            			"seasons": 20,
            			"trailer": "gogle.com.br",
            			"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
            			"views": 5,
            			"dubbed": false,
            			"subtitle": true,
            			"classification": 18,
            			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
            		}
            	]
            }, 200
            
            ```
            

- **GENDERS**
    - **POST** /genders
        - Rota protegida, apenas administradores
        - Formato da requisição
        
        ```json
        {
         "gender": "Ação"
        }
        ```
        
        - Retorno da requisição 201 (CREATED)
        
        ```json
        {
         "id": 1
         "gender": "ação"
        }, 201
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['gender']"
        }
        ```
        
        - Retorno da requisição caso já exista o genero, status code 400 (CONFLICT)
        
        ```json
        {
        	"error": "gender already exists"
        }
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
    - **GET** /genders
        - Rota deve ser privada
        - Retorno da requisição 200 (OK)
        
        ```json
        {
        	[
        		{
        			"id": 4,
        			"gender": "Ação"
        		},
        		{
        			"id": 8,
        			"gender": "Aventura"
        		},
        		{
        			"id": 3,
        			"gender": "Novo nome"
        		}
        	]
        }
        ```
        
    - **GET** /genders/<int:id>
        - Rota deve ser privada
        - Retorno da requisição
        
        ```json
        {
        	{"id": 1, "gender": "ação"},
        }
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Gender not found"
        }
        ```
        
    - **DELETE** /genders/<int:id>
        - Rota protegida, apenas administradores
        - Não passará nada na requisição
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Gender not found"
        }
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
    - **PATCH** /genders/<int:id>
        - Rota protegida, apenas administradores
        - Não passará nada na requisição
        - Formato da requisição
        
        ```json
        {
         "gender": "Novo nome"
        }
        ```
        
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['gender']"
        }
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Gender not found"
        }
        ```
        
        - Retorno da requisição caso já exista o genero, status code 400 (CONFLICT)
        
        ```json
        {
        	"error": "gender already exists"
        }
        ```
        

- **SERIES**
    - **Post** /series
        - Inclui uma série
        - Rota protegida, apenas administradores
        - formato da requisição
        
        ```json
        {
          "name": "Naruto",
        	"image": "www.google.com.png",
        	"description": "naruto um garoto com a raposa",
        	"seasons": 20,
        	"subtitle": true,
        	"dubbed": false,
        	"trailer": "gogle.com.br",
        	"classification": 18,
        	"released_date": "11/20/2022"
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        {
          "id": 8,
          "name": "One Change 3",
          "description": "naruto um garoto com a raposa",
          "image": "www.google.com.png",
          "seasons": 20,
          "trailer": "gogle.com.br",
          "created_at": "Thu, 10 Mar 2022 14:36:32 GMT",
          "views": 0,
          "dubbed": false,
          "subtitle": true,
          "classification": 18,
          "released_date": "Sat, 05 Nov 2022 00:00:00 GMT",
          "gender": [],
          "episodes": []
        }
        ```
        
        - Retorno da requisição caso não for administrador, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['name', 'image', 'description', 'seasons', 'subtitle', 'dubbed', 'trailer', 'classification', 'released_date']"
        }
        ```
        
        - Retorno da requisição caso já exista, status code 400 (BAD_REQUEST)
        
        ```json
        {
          "error": "This serie is already exists"
        }
        ```
        
    - **GET** /series
        - Todas as séries
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição. O perfil deve estar relacionado ao usuário logado.
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        [
        	{
        		"id": 10,
        		"name": "Naruto05",
        		"description": "naruto um garoto com a raposa",
        		"image": "www.google.com.png",
        		"seasons": 20,
        		"trailer": "gogle.com.br",
        		"created_at": "Wed, 02 Mar 2022 18:04:34 GMT",
        		"views": 0,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Wed, 11 May 2022 00:00:00 GMT",
        		"gender": [],
        		"episodes": []
        	},
        	{
        		"id": 6,
        		"name": "Naruto03",
        		"description": "naruto um garoto com a raposa",
        		"image": "www.google.com.png",
        		"seasons": 20,
        		"trailer": "gogle.com.br",
        		"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
        		"views": 5,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Wed, 11 May 2022 00:00:00 GMT",
        		"gender": [
        			{
        				"id": 4,
        				"gender": "Ação"
        			}
        		],
        		"episodes": [
        			{
        				"season": 2,
        				"link": "www.dsadsadsad.com",
        				"episode": 324
        			},
        			{
        				"season": 2,
        				"link": "www.dsadsadsad.com",
        				"episode": 324
        			}
        		]
        	}
        ]
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /series/<int:id>
        - Um série referente ao id descrito
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição. O perfil deve estar relacionado ao usuário logado.
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta  200 (OK)
        
        ```json
        {
        	"id": 6,
        	"name": "Naruto03",
        	"description": "naruto um garoto com a raposa",
        	"image": "www.google.com.png",
        	"seasons": 20,
        	"trailer": "gogle.com.br",
        	"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
        	"views": 5,
        	"dubbed": false,
        	"subtitle": true,
        	"classification": 18,
        	"released_date": "Wed, 11 May 2022 00:00:00 GMT",
        	"gender": [
        		{
        			"id": 4,
        			"gender": "Ação"
        		}
        	],
        	"episodes": [
        		{
        			"season": 2,
        			"link": "www.dsadsadsad.com",
        			"episode": 324
        		},
        		{
        			"season": 2,
        			"link": "www.dsadsadsad.com",
        			"episode": 324
        		}
        	]
        }
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
        Formato de resposta caso não exista serie com o id indicado ou seja inapropriado para a idade do perfil da requisição, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"message": "Serie not found"
        }
        ```
        
    - **PATCH** /series/<int:id>
        - Atualiza informações da série de id indicado
        
        Corpo da requisição pode conter as seguintes chaves: 
        
        "name",
        "image",
        "description",
        "seasons",
        "subtitle",
        "dubbed",
        "trailer",
        "classification",
        "released_date"
        
        Exemplo:
        
        ```json
        {
          "image": "www.google.com.png",
        	"description": "naruto um garoto com a raposa",
        	"seasons": 20,
        	"subtitle": true,
        	"dubbed": false,
        	"trailer": "gogle.com.br",
        	"classification": 18
        }
        ```
        
        - Retorno esperado, sucesso sem conteúdo 204(NO_CONTENT)
        
        ```json
        {}
        ```
        
        - Retorno da requisição caso não for administrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
        - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Must contain the keys: ['name', 'image', 'description', 'seasons', 'subtitle', 'dubbed', 'trailer', 'classification', 'released_date']"
        }
        ```
        
        - Retorno da requisição caso não encontre a série com o id indicado, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Serie not found"
        }
        ```
        
    - **GET /**series/name?name=name_to_search
        - Todos as séries que tenham determinada palavra
        - Deve ter o id do perfil no corpo da requisição. O perfil deve estar relacionado ao usuário logado.
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        {
        	"id": 3,
        	"name": "Naruto01",
        	"description": "naruto um garoto com a raposa",
        	"image": "www.google.com.png",
        	"seasons": 20,
        	"trailer": "gogle.com.br",
        	"created_at": "Wed, 02 Mar 2022 10:38:33 GMT",
        	"views": 0,
        	"dubbed": false,
        	"subtitle": true,
        	"classification": 18,
        	"released_date": "Wed, 11 May 2022 00:00:00 GMT",
        	"episodes": []
        }
        ```
        
        Caso não seja passada a query “name”, retornará uma mensagem de erro, 404 (NOT_FOUND)
        
        ```json
         {"error": "The query 'name' is necessary to search by name"}
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /series/most_seen
        - As 5 primeiras séries mais assistidos
        - rota dos  5 mais vistos
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição. O perfil deve estar relacionado ao usuário logado.
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        {
        	[
        		{
        			"id": 6,
        			"name": "Naruto03",
        			"image": "www.google.com.png",
        			"description": "naruto um garoto com a raposa",
        			"seasons": 20,
        			"trailer": "gogle.com.br",
        			"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
        			"views": 5,
        			"dubbed": false,
        			"subtitle": true,
        			"classification": 18,
        			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
        		},
        		{
        			"id": 10,
        			"name": "Naruto05",
        			"image": "www.google.com.png",
        			"description": "naruto um garoto com a raposa",
        			"seasons": 20,
        			"trailer": "gogle.com.br",
        			"created_at": "Wed, 02 Mar 2022 18:04:34 GMT",
        			"views": 0,
        			"dubbed": false,
        			"subtitle": true,
        			"classification": 18,
        			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
        		}
        	]
        }, 200
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /series/recents
        - Em até 5 séries em ordem decrescente de lançamento
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição. O perfil deve estar relacionado ao usuário logado.
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta, 200 (OK)
        
        ```json
        {
        	[
        		{
        			"id": 1,
        			"name": "Naruto",
        			"image": "www.enderco.com",
        			"description": "",
        			"seasons": 3,
        			"subtitle": "o maior ninja do mundo",
        			"views": 824,
        			"dubled": True,
        			"trailer": ""
        		},
        		{
        			"id": 2,
        			"name": "Boruto",
        			"image": "www.endereco.com",
        			"description": "",
        			"seasons": 3,
        			"subtitle": "a próxima geração",
        			"views": 404,
        			"dubled": False,
        			"trailer": ""
        		}
        	]
        }
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /series/genre?genre=genre_name
        - Todos as séries de um determinado gênero
        - Rota deve ser privada
        - Esta rota entrega todos os filmes de um determinado gênero
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta, 200 (OK)
        
        ```json
        [{
        	"id": 1,
        	"name": "One Piece1",
        	"image": "www.google.com.png",
        	"description": "naruto um garoto com a raposa",
        	"seasons": 20,
        	"trailer": "gogle.com.br",
        	"created_at": "Tue, 08 Mar 2022 14:15:27 GMT",
        	"views": 0,
        	"dubbed": false,
        	"subtitle": true,
        	"classification": 11,
        	"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
        },{
        		"id": 2,
        		"name": "One Piece2",
        		"image": "www.google.com.png",
        		"description": "naruto um garoto com a raposa",
        		"seasons": 20,
        		"trailer": "gogle.com.br",
        		"created_at": "Tue, 08 Mar 2022 14:15:27 GMT",
        		"views": 0,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 11,
        		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
        	}
        ...
        ]
        ```
        
        - Retorno da requisição caso não seja encontrado o gênero com o nome enviado,  404 (NOT_FOUND)
        
        ```json
        {
        	"Error": "Genre not found"
        }
        ```
        
        Caso não seja passada a query “genre” retornará uma mensagem de erro, 404 (BAD_REQUEST)
        
        ```json
         {"error": "The query 'genre' is necessary to search by genre"}
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **DELETE** /series/<int:id>
        - Deleta a série do id indicado
        - Rota protegida, apenas administradores
        - Requisição
        - 
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "serie not found"
        }
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
    - **POST** /series/favorite
        - Adiciona uma série aos favoritos de um perfil
        - Rota deve ser privada
        - formato da requisição
        
        ```json
        {
        	"profile_id": 5,
        	"serie_id": 6
        }
        ```
        
        - Formato da resposta, 200 (OK)
        
        ```json
        {}, 204
        ```
        
        - Formato quando profile não existentes,  404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Profile not found"
        }
        ```
        
        - Formato quando serie não existente ou é inapropriada para o perfil solicitado,  404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Serie not found"
        }
        ```
        
        - Formato quando profile não pertence ao user autenticado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
        - Formato quando já é favorito, 401 (CONFLICT)
        
        ```json
        {
        	"error": "Is already favorite"
        }
        ```
        
    - **DELETE** /series/favorite
        - Remove uma série dos favoritos de um perfil
        - Rota deve ser privada
        - formato da requisição
        
        ```json
        {
        	"profile_id": 5,
        	"serie_id": 6
        }
        ```
        
        - Formato da resposta
        
        ```json
        {}, 204
        ```
        
        - Formato da resposta quando profile não tem associação   404 (NOT_FOUND)
        
        ```json
        {
          "error": "Serie not found in profile"
        }, 404
        ```
        
        - Formato da resposta com profile não existentes,   404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Profile not found"
        }
        ```
        
        - Formato da resposta com serie não existentes,  404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Serie not found"
        }
        ```
        
        - Formato da quando profile não pertence ao user autenticado 401 (UNAUTHORIZED)
        
        ```json
        {
          "error": "Invalid profile for user"
        }
        ```
        
    - **GENDER**
        - **POST/series/gender**
            - Adiciona uma série à um gênero
            - Rota protegida, apenas administradores
            - formato da requisição
            
            ```json
            {
            	"gender_id": 5,
            	"serie_id": 6
            }
            ```
            
            - Formato da resposta
            
            ```json
            {}, 204
            ```
            
            - Formato da resposta com gender não existentes, type 404
            
            ```json
            {
            	"error": "Gender not found"
            }
            ```
            
            - Formato da resposta com serie não existentes, type 404
            
            ```json
            {
            	"error": "Serie not found"
            }
            ```
            
        - **DELETE**/series/gender
            - Remove uma série de um gênero
            - Rota protegida, apenas administradores
            - formato da requisição
            
            ```json
            {
            	"gender_id": 5,
            	"serie_id": 6
            }
            ```
            
            - Formato da resposta  204 (NO_CONTENT)
            
            ```json
            {}, 204
            ```
            
            - Formato da resposta quando genre não é encontrado  404 (NOT_FOUND)
            
            ```json
            {
              "error": "Genre not found"
            }
            ```
            
            - Formato da resposta com serie não associada ao gênero,  404 (NOT_FOUND)
            
            ```json
            {
            	"error": "This serie does not belong to the genre"
            }
            ```
            
        

- **EPISODES**
    - **POST** /episodes
        - Rota protegida, apenas administradores
        - formato da requisição
        
        ```json
        {
          "season": 1,
        	"link": "www.dsadsadsad.com",
        	"series_id": 1,
        	"episode": 324
        }
        ```
        
        - Formato da resposta
        
        ```json
        {
        	"id": 2,
        	"season": 1,
        	"link": "www.dsadsadsad.com",
        	"episode": 324,
        	"series_id": 1
        }
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
    - **GET** /episodes
        - Rota deve ser privada
        - Formato da resposta
        
        ```json
        [
        	{
        		"id": 1,
        		"season": 1,
        		"link": "www.dsadsadsad.com",
        		"episode": 324,
        		"series_id": 1
        	},
        	{
        		"id": 2,
        		"season": 1,
        		"link": "www.dsadsadsad.com",
        		"episode": 324,
        		"series_id": 1
        	},
        	{
        		"id": 3,
        		"season": 2,
        		"link": "www.dsadsadsad.com",
        		"episode": 324,
        		"series_id": 3
        	},
        	{
        		"id": 5,
        		"season": 2,
        		"link": "www.dsadsadsad.com",
        		"episode": 324,
        		"series_id": 6
        	}
        ]
        ```
        
    - **GET** /episodes/<int:id>
        - Rota deve ser privada
        - Formato da resposta
        
        ```json
        {
        	"id": 1,
        	"season": 1,
        	"link": "www.dsadsadsad.com",
        	"episode": 324,
        	"series_id": 1
        }
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "episode not found"
        }
        ```
        
    - **DELETE** /episodes/<int:id>
        - Rota protegida, apenas administradores
        - Requisição
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso não for adimistrador, status code 400 (BAD_REQUEST)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        

- **MOVIES**
    - **POST** /movies
        - Rota protegida, apenas administradores
        - Corpo da requisição
            
            ```json
            {
            	"name": "Título do filme",
            	"image": "google.png",
            	"description": "Essa é a histório  do filme que vem no exemplo...",
            	"duration": 120,
            	"subtitle": true,
            	"dubbed": false,
            	"link": "www.youtube.com.br/lasjdoasdasoidje",
            	"trailers": "www.trailler.com",
            	"classification": 18,
            	"released_date": "01/11/2000"
            	}
            ```
            
        - Retorno da requisição 200 (OK)
            
            ```json
            {
            	"id": 10,
            	"name": "Título Do Filme",
            	"image": "google.png",
            	"description": "Essa é a histório  do filme que vem no exemplo...",
            	"duration": 120,
            	"link": "www.youtube.com.br/lasjdoasdasoidje",
            	"trailers": "www.trailler.com",
            	"created_at": "Tue, 08 Mar 2022 11:07:41 GMT",
            	"views": 0,
            	"dubbed": false,
            	"subtitle": true,
            	"classification": 18,
            	"released_date": "Tue, 11 Jan 2000 00:00:00 GMT"
            }
            ```
            
            - Retorno da requisição caso não for administrador, status code 401 (UNAUTHORIZED)
            
            ```json
            {
            	"error": "Admins only"
            }
            ```
            
            - Retorno da requisição caso alguns dos campos estejam errados, status code 400 (BAD_REQUEST)
            
            ```json
            {
            	"error": "Must contain the keys: ['name', 'image', 'description', 'duration', 'trailers', 'link', 'subtitle', 'dubbed', 'classification', 'released_date']"
            }
            ```
            
        
    - **GET** /movies
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        [
        	{
        		"id": 2,
        		"name": "Naruto02",
        		"image": "www.google.com.png",
        		"description": "naruto um garoto com a raposa",
        		"duration": 10,
        		"link": "gogle.com.br",
        		"trailers": "gogle.com.br",
        		"created_at": "Tue, 08 Mar 2022 14:17:07 GMT",
        		"views": 0,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT",
        		"gender": [
        			{
        				"id": 1,
        				"gender": "Aventura"
        			},
        			{
        				"id": 2,
        				"gender": "Comedia"
        			}
        		]
        	},
        	{
        		"id": 3,
        		"name": "Naruto03",
        		"image": "www.google.com.png",
        		"description": "naruto um garoto com a raposa",
        		"duration": 10,
        		"link": "gogle.com.br",
        		"trailers": "gogle.com.br",
        		"created_at": "Tue, 08 Mar 2022 14:17:07 GMT",
        		"views": 0,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT",
        		"gender": [
        			{
        				"id": 3,
        				"gender": "Terror"
        			}
        		]
        	},
        	...
        ]
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
    - **GET** /movies/<int:id>
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta,  200 (OK)
        
        ```json
        {
        	"id": 6,
        	"name": "Naruto03",
        	"description": "naruto um garoto com a raposa",
        	"image": "www.google.com.png",
        	"seasons": 20,
        	"trailer": "gogle.com.br",
        	"created_at": "Wed, 02 Mar 2022 12:15:36 GMT",
        	"views": 5,
        	"dubbed": false,
        	"subtitle": true,
        	"classification": 18,
        	"released_date": "Wed, 11 May 2022 00:00:00 GMT",
        	"gender": [
        		{
        			"id": 4,
        			"gender": "Ação"
        		}
        	],
        	"episodes": [
        		{
        			"season": 2,
        			"link": "www.dsadsadsad.com",
        			"episode": 324
        		},
        		{
        			"season": 2,
        			"link": "www.dsadsadsad.com",
        			"episode": 324
        		}
        	]
        }
        ```
        
        - Retorno da requisição caso id não exista ou seja inapropriado para o perfil da requisição, status code 404 (NOT_FOUND)
        
        ```json
        {"error": "Movie not found"}
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
    - **PATCH** /movies/<int:id>
        - Corpo da requisição pode conter as seguintes chaves:
            
            "name",
            "image",
            "description",
            "seasons",
            "subtitle",
            "dubbed",
            "trailer",
            "classification",
            "released_date",
            "duration",
            "link",
            
            Exemplo:
            
        
        ```json
        {
        	"image": "google.jpg",
        	"description": "Essa é a a nova história  do filme que vem no exemplo...",
        	"duration": 120,
        	"link": "www.youtube.com.br/lasjdoasdasoidje"
        	}
        ```
        
        - Retorno esperado, sucesso sem conteúdo 204(NO_CONTENT)
        
        ```json
        {não está salvando}
        ```
        
        - Retorno da requisição caso não for administrador, status code 401 (UNAUTHORIZED)
        
        ```json
        {"error": "Admins only"}
        ```
        
        - Retorno da requisição caso não encontre a filme com o id indicado, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "movie not found"
        }
        ```
        
        - Retorno da requisição caso haja chave não errada, status code 400 (BAD REQUEST)
        
        ```json
        {
          "error": "Must contain the keys: ['image', 'description', 'duration', 'trailers', 'link', 'subtitle', 'dubbed', 'classification']"
        }
        ```
        
    - **DELETE** /movies/<int:id>
        - Rota protegida, apenas administradores
        - Retorno da requisição 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Retorno da requisição caso id não exista, status code 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "movie not found"
        }
        ```
        
        - Retorno da requisição caso o user não seja administer, status code 401 (UNAUTHORIZED)
        
        ```json
        {"error": "Admins only"}
        ```
        
    - **POST/movies/genre**
        - Rota protegida, apenas administradores
        - formato da requisição
        
        ```json
        {
        	"genre_id": 5,
        	"movie_id": 6
        }
        ```
        
        - Formato da resposta 204 (CREATED)
        
        ```json
        {}, 204
        ```
        
        - Formato da resposta com genre não existente, 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Gender not found"
        }
        ```
        
        - Formato da resposta com movie não existente, 404 (NOT_FOUND)
        
        ```json
        {
        	"error": "Movie not found"
        }
        ```
        
        - Retorno da requisição caso o usuário não seja administrador, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Admins only"
        }
        ```
        
    - **GET** /movies/genre?genre=genre_name
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato de resposta, 200 (OK)
            
            ```json
            [
            	{
            		"id": 1,
            		"name": "Naruto08",
            		"image": "www.google.com.png",
            		"description": "naruto um garoto com a raposa",
            		"duration": 10,
            		"link": "gogle.com.br",
            		"trailers": "gogle.com.br",
            		"created_at": "Tue, 08 Mar 2022 14:15:27 GMT",
            		"views": 0,
            		"dubbed": false,
            		"subtitle": true,
            		"classification": 18,
            		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
            	},
            	{
            		"id": 2,
            		"name": "Naruto02",
            		"image": "www.google.com.png",
            		"description": "naruto um garoto com a raposa",
            		"duration": 10,
            		"link": "gogle.com.br",
            		"trailers": "gogle.com.br",
            		"created_at": "Tue, 08 Mar 2022 14:17:07 GMT",
            		"views": 0,
            		"dubbed": false,
            		"subtitle": true,
            		"classification": 18,
            		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
            	}
            ]
            ```
            
            - Em caso de gênero inexistente, 404 (NOT_FOUND)
            
            ```json
            {
            	"Error": "Genre not found"
            }
            ```
            
            Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
            
            ```json
            {"error": "Profile not found"}
            ```
            
            Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
            
            ```json
            {
            	"error": "Invalid profile for user"
            }
            ```
            
    - **DELETE**/movies/genre
        - Rota protegida, apenas administradores
        - formato da requisição
        
        ```json
        {
        	"genre_id": 5,
        	"movie_id": 3
        }
        ```
        
        - Formato da resposta 204 (NO_CONTENT)
        
        ```json
        {}, 204
        ```
        
        - Formato da resposta quando genre não tem associação,  404 (NOT_FOUND)
        
        ```json
        {
        	"error": "This movie does not belong to the genre"
        }
        ```
        
        - Formato da resposta quando genre não é encontrado  404 (NOT_FOUND)
        
        ```json
        {
          "error": "Genre not found "
        }
        ```
        
    - **GET** /movies/most_seen
        - rota dos  5 mais vistos
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        {
        	[
        		{
        			"id": 4,
        			"name": "Naruto06",
        			"image": "www.google.com.png",
        			"description": "naruto um garoto com a raposa",
        			"duration": 10,
        			"link": "gogle.com.br",
        			"trailers": "gogle.com.br",
        			"created_at": "Fri, 04 Mar 2022 11:10:55 GMT",
        			"views": 200,
        			"dubbed": false,
        			"subtitle": true,
        			"classification": 18,
        			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
        		},
        		{
        			"id": 3,
        			"name": "OnePiece",
        			"image": "www.google.com.png",
        			"description": "naruto um garoto com a raposa",
        			"duration": 10,
        			"link": "gogle.com.br",
        			"trailers": "gogle.com.br",
        			"created_at": "Fri, 04 Mar 2022 11:10:55 GMT",
        			"views": 101,
        			"dubbed": false,
        			"subtitle": true,
        			"classification": 18,
        			"released_date": "Wed, 11 May 2022 00:00:00 GMT"
        		}
        	]
        }, 200
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /movies/recents
        - Rota deve ser privada
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato da resposta 200 (OK)
        
        ```json
        {
        	[
        	{
        		"id": 10,
        		"name": "Título Do Filme",
        		"image": "google.png",
        		"description": "Essa é a histório  do filme que vem no exemplo...",
        		"duration": 120,
        		"link": "www.youtube.com.br/lasjdoasdasoidje",
        		"trailers": "www.trailler.com",
        		"created_at": "Tue, 08 Mar 2022 11:07:41 GMT",
        		"views": 5,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Tue, 11 Jan 2000 00:00:00 GMT"
        	},
        	{
        		"id": 9,
        		"name": "Naruto09",
        		"image": "www.google.com.png",
        		"description": "naruto um garoto com a raposa",
        		"duration": 10,
        		"link": "gogle.com.br",
        		"trailers": "gogle.com.br",
        		"created_at": "Tue, 08 Mar 2022 11:06:36 GMT",
        		"views": 4,
        		"dubbed": false,
        		"subtitle": true,
        		"classification": 18,
        		"released_date": "Wed, 11 May 2022 00:00:00 GMT"
        	}
        	]
        }
        ```
        
        Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
        
        ```json
        {"error": "Profile not found"}
        ```
        
        Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
        
        ```json
        {
        	"error": "Invalid profile for user"
        }
        ```
        
    - **GET** /movies/name?name=name_to_search
        - Rota deve ser privada
        - Requisição
        - Deve ter o id do perfil no corpo da requisição
        
        ```json
        {
        "profile_id": 8
        }
        ```
        
        - Formato de resposta  200 (OK)
            
            ```json
            [
            	{
            		"id": 1,
            		"name": "Naruto08",
            		"image": "www.google.com.png",
            		"description": "naruto um garoto com a raposa",
            		"duration": 10,
            		"link": "gogle.com.br",
            		"trailers": "gogle.com.br",
            		"created_at": "Tue, 08 Mar 2022 14:15:27 GMT",
            		"views": 0,
            		"dubbed": false,
            		"subtitle": true,
            		"classification": 18,
            		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
            	},
            	{
            		"id": 2,
            		"name": "Naruto02",
            		"image": "www.google.com.png",
            		"description": "naruto um garoto com a raposa",
            		"duration": 10,
            		"link": "gogle.com.br",
            		"trailers": "gogle.com.br",
            		"created_at": "Tue, 08 Mar 2022 14:17:07 GMT",
            		"views": 0,
            		"dubbed": false,
            		"subtitle": true,
            		"classification": 18,
            		"released_date": "Sat, 05 Nov 2022 00:00:00 GMT"
            	},
            	...
            ]
            ```
            
            Caso não seja passada a query “name”, retornará uma mensagem de erro, 404 (NOT_FOUND)
            
            ```json
            {
            	"error": "The query 'name' is necessary to search by name"
            }
            ```
            
            Retorno da requisição caso o perfil não exista, status code  404 (NOT_FOUND)
            
            ```json
            {"error": "Profile not found"}
            ```
            
            Retorno da requisição caso o perfil não esteja relacionado com o usuário logado, status code 401 (UNAUTHORIZED)
            
            ```json
            {
            	"error": "Invalid profile for user"
            }
            ```
            
    - **FAVORITE**
        - **POST** /movies/favorite/
            - Rota deve ser privada
            - formato da requisição
            
            ```json
            {
            	"profile_id": 5,
            	"movie_id": 6
            }
            ```
            
            - Formato da resposta 204(NO_CONTENT)
            
            ```json
            {}, 204
            ```
            
            - Formato da resposta com profile não existente,  404(NOT_FOUND)
            
            ```json
            {
            	"error": "Profile not found"
            }
            ```
            
            - Formato da resposta com ou filme não existentes, 404(NOT_FOUND)
            
            ```json
            {
            	"error": "Movie not found"
            }
            ```
            
            - Formato da resposta quando profile não pertence ao user autenticado 401(UNAUTHORIZED)
            
            ```json
            {
            	"error": "Invalid profile for user"
            }
            ```
            
        - **DELETE** /movies/favorite_remove/
            - Rota deve ser privada
            - formato da requisição
            
            ```json
            {
            	"profile_id": 5,
            	"movie_id": 6
            }
            ```
            
            - Formato da resposta 204(NO_CONTENT)
            
            ```json
            {}, 204
            ```
            
            - Formato da resposta quando profile não tem associação  404(NOT_FOUND)
            
            ```json
            {
              "error": "Movie not found in favorite's profile"
            }
            ```
            
            - Formato da resposta com profile não existentes,   404(NOT_FOUND)
            
            ```json
            {
            	"error": "Profile not found"
            }
            ```
            
            - Formato da resposta com movie não existentes, 404(NOT_FOUND)
            
            ```json
            {
            	"error": "Movie not found"
            }
            ```
            
            - Formato da quando profile não pertence ao user autenticado  401(UNAUTHORIZED)
            
            ```json
            {
              "error": "Invalid profile for user"
            }
            ```