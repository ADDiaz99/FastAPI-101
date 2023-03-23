from fastapi import FastAPI        
from fastapi.responses import HTMLResponse, JSONResponse        
from pydantic import BaseModel                           
from utils.jwt_manager import create_token
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router
#Body permite escribir datos en el body instead of requirements, y path para dar caracteristicas a la ruta de donde salga algo
#HTMLResponse es para integrar un codigo html en una respuesta 
#BaseModel es para hacer una clase para las peliculas, Field es para dar caracteristicas a la clase   
#Optional permite establecer una condicion como opcional
#HTTPBearer permite validar las credenciales de un token

app = FastAPI()
app.title = 'Primera app - FastAPI'
app.version = '0.0.1'

app.add_middleware(ErrorHandler) #Agregamos el error handler
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

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
    return HTMLResponse('<h1>FastAPI Project!</h1>')

