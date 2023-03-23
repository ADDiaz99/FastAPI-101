from pydantic import BaseModel, Field                           
from typing import Optional  



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
