from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends         
from fastapi.responses import HTMLResponse, JSONResponse        
from pydantic import BaseModel, Field                           
from typing import Optional, List                                            
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

#Body permite escribir datos en el body instead of requirements, y path para dar caracteristicas a la ruta de donde salga algo
#HTMLResponse es para integrar un codigo html en una respuesta 
#BaseModel es para hacer una clase para las peliculas, Field es para dar caracteristicas a la clase   
#Optional permite establecer una condicion como opcional
#HTTPBearer permite validar las credenciales de un token

app = FastAPI()
app.title = 'Primera app - FastAPI'
app.version = '0.0.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail= "Las Credenciales No Son Validas")
    
class User(BaseModel):
    email: str 
    password: str

class Movie(BaseModel):
    id: Optional[int] | None = None
    title: str = Field(min_length=2, max_length=15)
    overview: str = Field(min_length= 2, max_length= 50)
    year: int = Field(le= 2024) #Al ser un int, para limitarlo se utiliza 'le', que significa 'lesser or equal than'
    rating: float = Field(ge= 1, le= 10) #ge significa 'greater or equal than'
    category: str = Field(min_length= 2, max_length= 15)

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'title': 'Titulo',
                'overview': 'Descripcion de la Pelicula',
                'year': 2024,
                'rating': 9.5,
                'category': 'Suspenso',
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, 
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]


@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags= ['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content= token)

@app.get('/movies', tags=['movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge= 1, le= 2000)) -> Movie:  #Un ejemplo del uso del path, para dar caracteristicas a una funcion
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category ]
    return JSONResponse(content=[data])

@app.post('/movies', tags=['movies'], response_model= dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})
  
@app.put('/movies/{id}', tags=['movies'], response_model= dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == movie.id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

@app.delete('/movies/{id}', tags=['movies'], response_model= dict, status_code=200)
def delete_movie(id: int) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})