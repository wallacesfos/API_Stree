filtros -> path
perfil -> body
user -> body



## REGRAS DE NEGÓCIO:
-Todas as requisições get estarão submetidas à um perfil associado à um usuário.
-As requisições do perfil entregam conteúdos de acordo com a sua classificação kids.
-Todas as requisições de obras deverão ser autenticadas.

-A rota de criar usuário é pública. Qualquer um pode criar um usuário.
-A rota de criar perfil é privada. Um único usuário pode criar até 4 perfis.
-O usuário só poderá acessar os conteúdos sob um perfil definido.

-Um perfil pode ter infinitas obras favoritas entre séries e filmes.

-Um usuário só poderá se tornar um usuário administrador por alteração direta do desenvolvedor no banco de dados.

-Usuários não administradores poderão:
    -criar perfis
    -alterar nome e estado de kids do perfil
    -deletar um perfil
    -adicionar, sob um id de um perfil, series e filmes aos favoritos
    -remover, sob um id de um perfil, series e filmes dos favoritos
    -acessar todas as obras filmes e séries
    -acessar obras filtradas por nome
    -acessar obras filtradas por gênero
    -acessar obras filtradas por mais vistos
    -acessar obras fitlradas por mais recentes adicionadas ao catálogo
    -acessar obras filtradas por favoritos de um perfil
    -acessar episódios de uma determinada série
    -acessar obra, filme ou série, por ID


-Usuários administradores poderão:
    -todas as funções do não administradores
    -adicionar filmes e séries ao catálogo
    -alterar informações de um filme ou série
    -remover filmes e séries do catálogo
    -adicionar gênero à lista de gêneros
    -remover gênero da lista de gêneros
    -associar um gênero à um filme ou série
    -dessacioar um gênero de um filme ou série
    -adicionar episódio à uma série
    -deletar episódio de uma série



POST - /movies                                      Inclui um filme
POST - /movies/genre                                Adiciona um filme à um gênero
POST - /movies/favorite                             Adiciona um filme aos favoritos de um perfil

GET - /movies                                       Todos os filmes
GET - /movies/name/<name_to_search>                 Todos os filmes que tenham determinada palvra
GET - /movies/genre/<genre_name>                    Todos os filmes de um determinado gênero
GET - /movies/most_seen                             Os 5 primeiros filmes mais assistidos
GET - /movies/most_recent                           Em até 5 filmes em ordem descrescente de lançamento
GET - /movies/<int:id>                              Um filme referente ao id descrito

PATCH - /movies/<int:id>                            Atualiza informações do filme de id indicado

DELETE - /movies/id/<int:id>                        Deleta o filme de id indicado
DELETE - /movies/gender                             Remove um filme de um gênero
DELETE - /movies/favorite                           Remove um filme dos favoritos de um perfil




<br/>
<br/>
<br/>
<br/>
<br/>
<br/>



#### Inclui um filme no banco de dados.
```http
POST /movies
```
Rota exclusiva para administrador.

Deve incluir no corpo da requisição as informações do filme:
```json
{
	"name": "Título do filme",
	"image": "google.png",
	"description": "Essa é a história do filme que vem no exemplo...",
	"duration": 120,
	"subtitle": true,
	"dubbed": false,
	"link": "www.youtube.com.br/lasjdoasdasoidje",
	"trailers": "www.trailler.com",
	"classification": 18,
	"released_date": "01/11/2000"
}
```

O retorno esperado:
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

Caso seja feita requisição por usuário não administrador será retornado um erro 401.
``` json
{
	"error": "Admins only"
}
```
Caso tenha algum erro nas chaves necessárias será retornado um erro 400.
``` json
{
	"error": "Must contain the keys: ['name', 'image', 'description', 'duration', 'trailers', 'link', 'subtitle', 'dubbed', 'classification', 'released_date']"
}
```
<br/>
<br/>

#### Retorna todos os filmes.
```http
GET /movies 
```
Deve constar o id do perfil na requisição
```json
 {
  "profile_id": 1
}
```
Retorno esperado:
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



GET - /movies/<int:id>                              Um filme referente ao id descrito
```json ```
PATCH - /movies/<int:id>                            Atualiza informações do filme de id indicado
DELETE - /movies/id/<int:id>                        Deleta o filme de id indicado

```json 
```
```json 
```
```json 
```
```json 
```
```json 
```
```json 
```
```json 
```

POST - /movies/genre                                Adiciona um filme à um gênero
GET - /movies/genre/<genre_name>                    Todos os filmes de um determinado gênero
DELETE - /movies/gender                             Remove um filme de um gênero

POST - /movies/favorite                             Adiciona um filme aos favoritos de um perfil
DELETE - /movies/favorite                           Remove um filme dos favoritos de um perfil


GET - /movies/name/<name_to_search>                 Todos os filmes que tenham determinada palvra
GET - /movies/most_seen                             Os 5 primeiros filmes mais assistidos
GET - /movies/most_recent                           Em até 5 filmes em ordem descrescente de lançamento


