from fastapi import APIRouter
from fastapi import Path, Query, Depends         
from fastapi.responses import JSONResponse        
from pydantic import BaseModel, Field                           
from typing import Optional, List  
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie
movie_router = APIRouter()



@movie_router.get('/movies', tags=['movies'], response_model= List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies() #db.query(MovieModel).all() 
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge= 1, le= 2000)) -> Movie:  #Un ejemplo del uso del path, para dar caracteristicas a una funcion
    db = Session()
    result = MovieService(db).get_movie(id)  #Filtramos por id, mostramos el primero
    if not result: 
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category) #Filtramos por categoria y usamos .all para devolver todos los resultados
    if not result:
        return JSONResponse(status_code=404, content={'message': "Categoria no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model= dict, status_code=201) #Ruta de registro
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la pelicula"})
  
@movie_router.put('/movies/{id}', tags=['movies'], response_model= dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model= dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})