from fastapi import (
    FastAPI, Body, Query, Path
)
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional



app = FastAPI(
    title='Aprendiendo FastApi',
    description='Un API en los primeros pasos',
    version='0.0.2',
)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Movie Description', min_length=5, max_length=90)
    year: int = Field(default=1981)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Movie Category', min_length=5, max_length=15)

movie1 = Movie(
    id=1,
    title='El Padrino',
    overview='El Padrino es una pelicula de 1972 dirigida por Francis Ford Copola...',
    year=1981,
    rating=9,
    category='Crimen'
)

movies = [movie1]
@app.get(path= '/', tags=['Inicio'])
def read_root():
    return HTMLResponse('<h1>Hello Movies</h1>')

@app.get(path= '/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get(path='/movies/{id}', tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=5, title='Movie Id')):
    movie: Movie = next((movie for movie in movies if movie.id == id), None)
    if movie:
        return JSONResponse(status_code=200, content={
            'message':  'Movie found',
            'movie': movie.model_dump()
        })
    return JSONResponse(status_code=404, content={
        'message': 'Movie not found',
    })

@app.get(path='/movies/', tags=['Movies'], status_code=200)
def get_movie_by_category(category: str = Query(min_len=5, max_length=15)):
    return category
@app.post(path='/movies', tags=['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(status_code=201, content={
        'message': 'Movie created',
        'movie': movie.model_dump()
    })

#Update a Movie
@app.put(path='/movies/{id}', tags=['Movies'])
def update_movie(id:int = Path(ge=1, le=100), movie:Movie=Body()):
    updated_movie: Movie = next((updated_movie for updated_movie in movies if updated_movie.id == id), None)

    if updated_movie:
        updated_movie.title = movie.title
        updated_movie.overview = movie.overview
        updated_movie.year = movie.year
        updated_movie.rating = movie.rating
        updated_movie.category = movie.category

        return JSONResponse(status_code=200, content={
            'message': 'Movie updated',
            'movie': updated_movie.model_dump()
        })
    return JSONResponse(status_code=404, content={
        'message': 'Movie not found',
    })

#Delete a Movie
@app.delete(path='/movies/{id}', tags=['Movies'], status_code=200)
def delete_movie(id: int = Path(ge=1, le=100, title='Movie Id')):
    movie: Movie = next((movie for movie in movies if movie.id == id), None)
    if movie:
        movies.remove(movie)
        return JSONResponse(status_code=200, content={
            'message': 'Movie deleted',
            'movie': movie.model_dump()
        })
    return JSONResponse(status_code=404, content={
        'message': 'Movie not found',
    })
